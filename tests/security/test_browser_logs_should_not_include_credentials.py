from res2jobworks_automation import capture_job, capture_text


def test_browser_logs_should_not_include_credentials(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    capture = capture_text(
        source_url="https://example.test/jobs/safe?token=live-token#access_token=secret",
        text="# Safe Analyst\n\n## Organization\nExample Labs\n",
        captured_at="2026-06-04T12:00:00Z",
    )

    envelope = capture_job(database_path, capture=capture)

    serialized = envelope.model_dump_json()
    assert "live-token" not in serialized.lower()
    assert "access_token" not in serialized.lower()
    assert "cookie" not in serialized.lower()
    assert "authorization" not in serialized.lower()
    assert "password" not in serialized.lower()
