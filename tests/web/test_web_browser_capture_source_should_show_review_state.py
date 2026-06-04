from apps.web.res2jobworks_web import render_dashboard_html

from res2jobworks_automation import capture_job, capture_text


def test_browser_capture_source_should_show_review_state(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    capture = capture_text(
        source_url="https://example.test/jobs/web",
        text="# Web Evidence Analyst\n\n## Organization\nExample Labs\n",
        captured_at="2026-06-04T12:00:00Z",
    )
    capture_job(database_path, capture=capture)

    html = render_dashboard_html(database_path)

    assert "Evidence source" in html
    assert "https://example.test/jobs/web" in html
    assert "Captured for human review" in html
