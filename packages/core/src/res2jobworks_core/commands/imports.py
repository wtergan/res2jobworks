"""Profile and job import workflows over canonical SQLite state."""

import sqlite3
from pathlib import Path

import yaml

from res2jobworks_core.commands._support import (
    extract_markdown_field,
    failure,
    first_markdown_heading,
    organization_name,
    read_source,
    required_text,
    slug,
    validate_public_text,
)
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def import_profile(
    database_path: Path | str,
    *,
    source_path: Path | str | None = None,
    source_text: str | None = None,
    source_type: str = "yaml",
    profile_id: str | None = None,
) -> CommandEnvelope:
    """Import one profile/resume source into canonical SQLite state."""
    command = "profile.import"
    inputs = {
        "database_path": str(database_path),
        "source_path": str(source_path) if source_path is not None else None,
        "source_type": source_type,
    }
    try:
        title, content = read_source(source_path=source_path, source_text=source_text)
        validate_public_text(content, source_type, "profile source")
        raw = yaml.safe_load(content)
        if not isinstance(raw, dict):
            raise ValueError("profile source must contain a mapping")
        display_name = required_text(raw, "name")
        resolved_profile_id = profile_id or f"profile-{slug(display_name)}"
        repository = SQLiteRepository(database_path)
        profile = repository.create_profile(
            profile_id=resolved_profile_id,
            display_name=display_name,
            headline=str(raw.get("headline", "")),
            summary=str(raw.get("summary", "")),
            skills=[str(skill) for skill in raw.get("skills", [])],
        )
        resume_source = repository.add_resume_source(
            source_id=f"{resolved_profile_id}-source-001",
            profile_id=profile["id"],
            source_type=source_type,
            title=title,
            content=content,
            metadata={"imported_by": command},
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"profile": profile, "resume_source": resume_source},
        )
    except (
        OSError,
        RepositoryError,
        sqlite3.Error,
        ValueError,
        yaml.YAMLError,
    ) as exc:
        return failure(command, inputs, exc)


def import_job(
    database_path: Path | str,
    *,
    source_path: Path | str | None = None,
    source_text: str | None = None,
    source_type: str = "markdown",
    job_id: str | None = None,
) -> CommandEnvelope:
    """Import a job description text or file into canonical SQLite state."""
    command = "jobs.import"
    inputs = {
        "database_path": str(database_path),
        "source_path": str(source_path) if source_path is not None else None,
        "source_type": source_type,
    }
    try:
        title, content = read_source(source_path=source_path, source_text=source_text)
        validate_public_text(content, source_type, "job source")
        job_title = (first_markdown_heading(content) or title).replace(
            "Fixture Job: ",
            "",
        )
        employer = organization_name(
            extract_markdown_field(content, "Organization") or "Unknown",
        )
        resolved_job_id = job_id or f"job-{slug(job_title)}"
        repository = SQLiteRepository(database_path)
        job = repository.create_job(
            job_id=resolved_job_id,
            employer=employer,
            title=job_title,
            location=extract_markdown_field(content, "Location") or "",
            description=content,
        )
        job_source = repository.add_job_source(
            source_id=f"{resolved_job_id}-source-001",
            job_id=job["id"],
            source_type=source_type,
            title=title,
            content=content,
            metadata={"imported_by": command},
        )
        warnings = []
        if employer == "Unknown":
            warnings.append("job source did not include an Organization section")
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"job": job, "job_source": job_source},
            warnings=warnings,
        )
    except (OSError, RepositoryError, sqlite3.Error, ValueError) as exc:
        return failure(command, inputs, exc)
