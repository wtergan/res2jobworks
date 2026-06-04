import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_export_with_windows_absolute_path_should_report_validation_error(
    tmp_path,
) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )

    with pytest.raises(RepositoryError, match="export path must be relative"):
        repository.record_export(
            export_id="export-1",
            export_type="job_snapshot",
            format="csv",
            target_table="jobs",
            target_id="job-1",
            path="C:\\Users\\alice\\private.csv",
        )
