from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_application_status_update_should_append_event(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )
    repository.create_application(
        application_id="application-1",
        job_id="job-1",
        status="interested",
        event_id="event-1",
    )

    application = repository.append_status_event(
        event_id="event-2",
        application_id="application-1",
        status="applied",
        note="Submitted after review",
    )

    assert application["current_status"] == "applied"
    assert [event["status"] for event in application["status_events"]] == [
        "interested",
        "applied",
    ]
