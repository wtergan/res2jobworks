from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_job_with_source_should_persist_and_reload(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    job = repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        location="Remote",
        description="Fictional fixture job description",
    )
    source = repository.add_job_source(
        source_id="job-source-1",
        job_id=job["id"],
        source_type="markdown_fixture",
        title="sample-job.md",
        content="Fictional fixture job description",
    )
    reloaded = repository.get_job("job-1")

    assert reloaded["employer"] == "Example Cooperative"
    assert reloaded["title"] == "Operations Analyst"
    assert source["job_id"] == "job-1"
