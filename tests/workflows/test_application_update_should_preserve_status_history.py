from res2jobworks_core.commands import add_application, update_application
from tests.workflows.helpers import import_public_fixture_pair


def test_application_update_should_preserve_status_history(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    _, job = import_public_fixture_pair(database_path)

    created = add_application(database_path, job_id=job["id"], status="interested")
    updated = update_application(
        database_path,
        application_id=created.data["application"]["id"],
        status="applied",
        note="Submitted after manual review.",
    )

    assert created.ok
    assert updated.ok
    application = updated.data["application"]
    assert application["current_status"] == "applied"
    assert [event["status"] for event in application["status_events"]] == [
        "interested",
        "applied",
    ]
    assert updated.data["status_event"]["note"] == "Submitted after manual review."
