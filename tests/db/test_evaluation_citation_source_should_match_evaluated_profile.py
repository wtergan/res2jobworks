import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_evaluation_citation_source_should_match_evaluated_profile(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_profile(profile_id="profile-1", display_name="Profile One")
    repository.create_profile(profile_id="profile-2", display_name="Profile Two")
    repository.add_resume_source(
        source_id="resume-source-2",
        profile_id="profile-2",
        source_type="yaml_fixture",
        title="profile-two.yaml",
        content="Fictional profile two fixture",
    )
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )

    with pytest.raises(RepositoryError, match="evaluation profile"):
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
                    "source_table": "resume_sources",
                    "source_id": "resume-source-2",
                    "quote": "Fictional profile two fixture",
                }
            ],
        )
