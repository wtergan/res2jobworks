"""Public fixture seeding for sample SQLite workspaces."""

from importlib import resources
from pathlib import Path
from typing import Any

import yaml

from res2jobworks_core.fixtures import validate_public_fixture_text
from res2jobworks_core.repositories.sqlite import SQLiteRepository

DEFAULT_PROFILE_ID = "fixture-profile-jordan-avery"
DEFAULT_RESUME_SOURCE_ID = "fixture-resume-source-jordan-avery"
DEFAULT_JOB_ID = "fixture-job-product-operations-analyst"
DEFAULT_JOB_SOURCE_ID = "fixture-job-source-product-operations-analyst"


def seed_public_sample_workspace(
    database_path: Path | str,
    *,
    profile_path: Path | None = None,
    job_path: Path | None = None,
) -> dict[str, Any]:
    """Create a migrated sample database from public-generic fixtures."""
    repository = SQLiteRepository(database_path)
    profile_text = _read_fixture_text(
        explicit_path=profile_path,
        packaged_name="profile-example.yaml",
        source_path=Path("templates/profile-example.yaml"),
    )
    job_text = _read_fixture_text(
        explicit_path=job_path,
        packaged_name="sample-job.md",
        source_path=Path("examples/jobs/sample-job.md"),
    )
    _validate_seed_fixture_text(profile_text, "profile fixture")
    _validate_seed_fixture_text(job_text, "job fixture")
    profile_data = yaml.safe_load(profile_text)
    if not isinstance(profile_data, dict):
        msg = "profile fixture must contain a mapping"
        raise ValueError(msg)

    profile = repository.create_profile(
        profile_id=DEFAULT_PROFILE_ID,
        display_name=str(profile_data["name"]),
        headline=str(profile_data.get("headline", "")),
        summary=str(profile_data.get("summary", "")),
        skills=[str(skill) for skill in profile_data.get("skills", [])],
    )
    resume_source = repository.add_resume_source(
        source_id=DEFAULT_RESUME_SOURCE_ID,
        profile_id=profile["id"],
        source_type="yaml_fixture",
        title=profile_path.name if profile_path else "profile-example.yaml",
        content=profile_text,
        metadata={"fixture": True},
    )

    title = _first_markdown_heading(job_text) or "Fixture Job"
    employer = (
        _extract_markdown_field(job_text, "Organization")
        or "Example Organization"
    )
    job = repository.create_job(
        job_id=DEFAULT_JOB_ID,
        employer=employer,
        title=title.replace("Fixture Job: ", ""),
        description=job_text,
        location="Remote",
    )
    job_source = repository.add_job_source(
        source_id=DEFAULT_JOB_SOURCE_ID,
        job_id=job["id"],
        source_type="markdown_fixture",
        title=job_path.name if job_path else "sample-job.md",
        content=job_text,
        metadata={"fixture": True},
    )

    return {
        "profile": profile,
        "resume_source": resume_source,
        "job": job,
        "job_source": job_source,
    }


def _read_fixture_text(
    *,
    explicit_path: Path | None,
    packaged_name: str,
    source_path: Path,
) -> str:
    if explicit_path is not None:
        return explicit_path.read_text(encoding="utf-8")

    packaged = resources.files("res2jobworks_core").joinpath(
        "fixtures",
        packaged_name,
    )
    if packaged.is_file():
        return packaged.read_text(encoding="utf-8")

    source_fixture = _find_source_fixture(source_path)
    return source_fixture.read_text(encoding="utf-8")


def _find_source_fixture(source_path: Path) -> Path:
    module_path = Path(__file__).resolve()
    for parent in module_path.parents:
        candidate = parent / source_path
        if candidate.is_file():
            return candidate
    msg = f"source fixture not found: {source_path}"
    raise FileNotFoundError(msg)


def _validate_seed_fixture_text(text: str, label: str) -> None:
    result = validate_public_fixture_text(text)
    if not result.ok:
        msg = f"{label} is not public-generic: {', '.join(result.errors)}"
        raise ValueError(msg)


def _first_markdown_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return None


def _extract_markdown_field(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    marker = f"## {heading}"
    for index, line in enumerate(lines):
        if line.strip() != marker:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if stripped:
                return stripped
    return None
