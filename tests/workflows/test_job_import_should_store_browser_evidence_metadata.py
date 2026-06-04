from res2jobworks_core.commands import import_job


def test_job_import_should_store_browser_evidence_metadata(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    source_text = "# Browser Captured Role\n\n## Organization\nExample Labs\n"

    envelope = import_job(
        database_path,
        source_text=source_text,
        source_type="browser_capture",
        source_url="https://example.test/jobs/123",
        source_metadata={
            "captured_at": "2026-06-04T12:00:00Z",
            "artifact_path": "captures/example-job.html",
        },
    )

    assert envelope.ok
    job_source = envelope.data["job_source"]
    assert job_source["source_url"] == "https://example.test/jobs/123"
    assert job_source["metadata"]["captured_at"] == "2026-06-04T12:00:00Z"
    assert job_source["metadata"]["artifact_path"] == "captures/example-job.html"
