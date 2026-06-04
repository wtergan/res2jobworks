from pathlib import Path

import pytest
from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job


@pytest.fixture
def evaluated_fixture_workspace(tmp_path: Path) -> dict:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluation_envelope = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )
    assert evaluation_envelope.ok
    return {
        "database_path": database_path,
        "profile": profile,
        "job": job,
        "evaluation": evaluation_envelope.data["evaluation"],
    }
