import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_application_evaluation_should_match_application_job(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_profile(profile_id="profile-1", display_name="Profile One")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job one",
    )
    repository.create_job(
        job_id="job-2",
        employer="Example Studio",
        title="Research Analyst",
        description="Fictional fixture job two",
    )
    repository.add_job_source(
        source_id="job-source-1",
        job_id="job-1",
        source_type="markdown_fixture",
        title="job-one.md",
        content="Fictional fixture job one",
    )
    repository.create_evaluation(
        evaluation_id="evaluation-1",
        profile_id="profile-1",
        job_id="job-1",
        rubric_version="mvp1",
        score=80,
        summary="Job one evaluation",
        recommendation="Review",
        citations=[
            {
                "source_table": "job_sources",
                "source_id": "job-source-1",
                "quote": "Fictional fixture job one",
            }
        ],
    )

    with pytest.raises(RepositoryError, match="same job"):
        repository.create_application(
            application_id="application-1",
            job_id="job-2",
            evaluation_id="evaluation-1",
            status="interested",
        )
