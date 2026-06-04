import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_missing_parent_record_should_report_repository_error(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    with pytest.raises(RepositoryError, match="profile does not exist"):
        repository.add_resume_source(
            source_id="resume-source-1",
            profile_id="missing-profile",
            source_type="yaml_fixture",
            title="profile.yaml",
            content="Fictional fixture profile",
        )
    with pytest.raises(RepositoryError, match="job does not exist"):
        repository.create_application(
            application_id="application-1",
            job_id="missing-job",
            status="interested",
        )
