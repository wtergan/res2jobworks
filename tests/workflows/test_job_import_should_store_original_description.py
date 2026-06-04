from pathlib import Path

from res2jobworks_core.commands import import_job
from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_job_import_should_store_original_description(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    source_path = Path("examples/jobs/sample-job.md")

    envelope = import_job(
        database_path,
        source_path=source_path,
        source_type="markdown_fixture",
    )

    assert envelope.ok
    job = envelope.data["job"]
    job_source = envelope.data["job_source"]
    assert job["title"] == "Product Operations Analyst"
    assert job["employer"] == "Northstar Civic Tools"
    assert "Basic familiarity with Python or SQL" in job["description"]
    assert job_source["job_id"] == job["id"]
    assert job_source["content"] == source_path.read_text(encoding="utf-8")
    assert SQLiteRepository(database_path).get_job(job["id"]) == job
