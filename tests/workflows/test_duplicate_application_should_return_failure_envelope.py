from res2jobworks_core.commands import add_application
from tests.workflows.helpers import import_public_fixture_pair


def test_duplicate_application_should_return_failure_envelope(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    _, job = import_public_fixture_pair(database_path)

    first = add_application(database_path, job_id=job["id"])
    second = add_application(database_path, job_id=job["id"])

    assert first.ok
    assert not second.ok
    assert second.command == "applications.add"
    assert second.errors[0].code == "IntegrityError"
