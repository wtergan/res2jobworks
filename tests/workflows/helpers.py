from pathlib import Path

from res2jobworks_core.commands import import_job, import_profile

REPO_ROOT = Path(__file__).resolve().parents[2]


def import_public_fixture_pair(database_path: Path) -> tuple[dict, dict]:
    profile_envelope = import_profile(
        database_path,
        source_path=REPO_ROOT / "templates/profile-example.yaml",
        source_type="yaml_fixture",
    )
    job_envelope = import_job(
        database_path,
        source_path=REPO_ROOT / "examples/jobs/sample-job.md",
        source_type="markdown_fixture",
    )
    assert profile_envelope.ok
    assert job_envelope.ok
    return profile_envelope.data["profile"], job_envelope.data["job"]
