from res2jobworks_core.commands import evaluate_job
from tests.workflows.helpers import import_public_fixture_pair


def test_duplicate_evaluation_should_return_failure_envelope(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)

    first = evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    second = evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])

    assert first.ok
    assert not second.ok
    assert second.command == "jobs.evaluate"
    assert second.errors[0].code == "IntegrityError"
