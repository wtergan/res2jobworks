from apps.tui.res2jobworks_tui import render_dashboard

from res2jobworks_automation import capture_job, capture_text


def test_browser_capture_source_should_show_review_state(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    capture = capture_text(
        source_url="https://example.test/jobs/tui\x1b[31m?token=secret",
        text=(
            "# TUI\x1b[31m Evidence Analyst\n\n"
            "## Organization\nExample\x1b[32m Labs\n"
        ),
        captured_at="2026-06-04T12:00:00Z",
    )
    capture_job(database_path, capture=capture)

    rendered = render_dashboard(database_path)

    assert "https://example.test/jobs/tui" in rendered
    assert "\x1b[" not in rendered
    assert "TUI Evidence Analyst" in rendered
    assert "Example Labs" in rendered
    assert "Captured for human review" in rendered
