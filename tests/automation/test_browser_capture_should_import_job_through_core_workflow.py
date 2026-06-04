from datetime import UTC, datetime

from res2jobworks_automation import CapturedJobSource, import_captured_job
from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_browser_capture_should_import_job_through_core_workflow(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    captured = CapturedJobSource(
        source_url="https://jobs.example.test/product-operations-analyst",
        title="Product Operations Analyst",
        text="# Product Operations Analyst\n\n## Organization\nExample Labs\n",
        captured_at=datetime(2026, 6, 4, 15, 30, tzinfo=UTC),
    )

    envelope = import_captured_job(database_path, captured, job_id="job-captured")

    assert envelope.ok
    assert envelope.command == "automation.capture_job"
    assert envelope.data["job"]["id"] == "job-captured"
    assert envelope.data["job"]["employer"] == "Example Labs"
    assert envelope.data["job_source"]["content"] == captured.text
    assert envelope.data["core_envelope"]["command"] == "jobs.import"
    assert SQLiteRepository(database_path).get_job("job-captured")["title"] == (
        "Product Operations Analyst"
    )
