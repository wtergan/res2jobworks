from datetime import UTC, datetime

from res2jobworks_automation import CapturedJobSource, import_captured_job
from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_evidence_capture_should_store_source_metadata(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    captured = CapturedJobSource(
        source_url="https://jobs.example.test/field-ops",
        title="Field Operations Coordinator",
        text="# Field Operations Coordinator\n\n## Organization\nExample Labs\n",
        captured_at=datetime(2026, 6, 4, 16, 45, tzinfo=UTC),
        screenshot_path="artifacts/captures/field-ops.png",
        artifact_paths=["artifacts/captures/field-ops.html"],
    )

    envelope = import_captured_job(database_path, captured, job_id="job-field-ops")

    assert envelope.ok
    job_source = SQLiteRepository(database_path).list_job_sources("job-field-ops")[0]
    assert job_source["source_url"] == captured.source_url
    assert job_source["metadata"] == {
        "artifact_paths": ["artifacts/captures/field-ops.html"],
        "captured_at": "2026-06-04T16:45:00+00:00",
        "evidence_kind": "browser_capture",
        "imported_by": "automation.capture_job",
        "screenshot_path": "artifacts/captures/field-ops.png",
        "source_title": "Field Operations Coordinator",
    }
