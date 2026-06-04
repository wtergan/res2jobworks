import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_application_status_should_be_known_value(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )

    with pytest.raises(RepositoryError, match="status must be one of"):
        repository.create_application(
            application_id="application-1",
            job_id="job-1",
            status="mystery",
        )
