from res2jobworks_core.repositories.sqlite import REDACTED, SQLiteRepository


def test_evaluation_provider_metadata_should_redact_secret_values(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_profile(profile_id="profile-1", display_name="Fictional User")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )
    repository.add_job_source(
        source_id="job-source-1",
        job_id="job-1",
        source_type="markdown_fixture",
        title="sample-job.md",
        content="Fictional fixture job description",
    )

    evaluation = repository.create_evaluation(
        evaluation_id="evaluation-1",
        profile_id="profile-1",
        job_id="job-1",
        rubric_version="mvp1",
        score=82,
        summary="Strong evidence-backed fit",
        recommendation="Prioritize",
        provider_metadata={"credential_blob": "secret", "safe_model": "fixture"},
        citations=[
            {
                "source_table": "job_sources",
                "source_id": "job-source-1",
                "quote": "Fictional fixture job description",
            }
        ],
    )

    assert evaluation["provider_metadata"]["credential_blob"] == REDACTED
    assert evaluation["provider_metadata"]["safe_model"] == "fixture"
