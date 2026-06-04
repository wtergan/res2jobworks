from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_repository_lists_should_return_core_records(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    profile = repository.create_profile(
        profile_id="profile-1",
        display_name="Fictional User",
    )
    job = repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )
    repository.add_job_source(
        source_id="job-source-1",
        job_id=job["id"],
        source_type="markdown_fixture",
        title="sample-job.md",
        content="Fictional fixture job description",
    )
    evaluation = repository.create_evaluation(
        evaluation_id="evaluation-1",
        profile_id=profile["id"],
        job_id=job["id"],
        rubric_version="mvp1",
        score=82,
        summary="Strong evidence-backed fit",
        recommendation="Prioritize",
        citations=[
            {
                "source_table": "job_sources",
                "source_id": "job-source-1",
                "quote": "Fictional fixture job description",
            }
        ],
    )
    application = repository.create_application(
        application_id="application-1",
        job_id=job["id"],
        evaluation_id=evaluation["id"],
        status="interested",
        event_id="event-1",
    )
    repository.record_export(
        export_id="export-1",
        export_type="tracker",
        format="csv",
        target_table="applications",
        target_id=application["id"],
        path="exports/tracker.csv",
    )
    repository.record_agent_run(
        run_id="agent-run-1",
        command_id="jobs.evaluate",
        status="completed",
    )

    assert [record["id"] for record in repository.list_profiles()] == ["profile-1"]
    assert [record["id"] for record in repository.list_jobs()] == ["job-1"]
    assert [record["id"] for record in repository.list_evaluations()] == [
        "evaluation-1"
    ]
    assert [record["id"] for record in repository.list_applications()] == [
        "application-1"
    ]
    assert [record["id"] for record in repository.list_exports()] == ["export-1"]
    assert [record["id"] for record in repository.list_agent_runs()] == [
        "agent-run-1"
    ]
