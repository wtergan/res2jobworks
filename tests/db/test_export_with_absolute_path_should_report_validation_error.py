from pathlib import Path

import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_export_with_absolute_path_should_report_validation_error(tmp_path) -> None:
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

    with pytest.raises(RepositoryError, match="export path must be relative"):
        repository.record_export(
            export_id="export-1",
            export_type="tracker",
            format="csv",
            target_table="applications",
            target_id="application-1",
            path=str(Path("/tmp/private/export.csv")),
        )
