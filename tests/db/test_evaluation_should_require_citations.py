import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_evaluation_should_require_citations(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_profile(profile_id="profile-1", display_name="Fictional User")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )

    with pytest.raises(RepositoryError, match="at least one citation"):
        repository.create_evaluation(
            evaluation_id="evaluation-1",
            profile_id="profile-1",
            job_id="job-1",
            rubric_version="mvp1",
            score=75,
            summary="Good fit",
            recommendation="Review",
            citations=[],
        )
