import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_evaluation_citation_source_should_match_evaluated_job(tmp_path) -> None:
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
        source_id="job-source-2",
        job_id="job-2",
        source_type="markdown_fixture",
        title="job-two.md",
        content="Fictional fixture job two",
    )

    with pytest.raises(RepositoryError, match="evaluation job"):
        repository.create_evaluation(
            evaluation_id="evaluation-1",
            profile_id="profile-1",
            job_id="job-1",
            rubric_version="mvp1",
            score=80,
            summary="Mismatched citation",
            recommendation="Reject",
            citations=[
                {
                    "source_table": "job_sources",
                    "source_id": "job-source-2",
                    "quote": "Fictional fixture job two",
                }
            ],
        )
