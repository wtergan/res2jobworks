import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_exports_should_reference_canonical_records(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )
    application = repository.create_application(
        application_id="application-1",
        job_id="job-1",
        status="interested",
        event_id="event-1",
    )

    export = repository.record_export(
        export_id="export-1",
        export_type="tracker",
        format="csv",
        target_table="applications",
        target_id=application["id"],
        path="exports/tracker.csv",
    )

    assert export["target_table"] == "applications"
    assert export["target_id"] == "application-1"
    with pytest.raises(RepositoryError, match="does not exist"):
        repository.record_export(
            export_id="export-2",
            export_type="tracker",
            format="csv",
            target_table="applications",
            target_id="missing",
            path="exports/missing.csv",
        )
