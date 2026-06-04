from res2jobworks_core.commands import evaluate_job
from tests.workflows.helpers import import_public_fixture_pair


def test_registry_declared_inputs_should_not_raise_type_error(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)

    envelope = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
        rubric_id="unsupported-rubric",
    )

    assert not envelope.ok
    assert envelope.errors[0].code == "ValueError"
    assert "unsupported rubric_id" in envelope.errors[0].message
