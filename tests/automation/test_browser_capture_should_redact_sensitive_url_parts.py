from res2jobworks_automation import capture_text


def test_browser_capture_should_redact_sensitive_url_parts() -> None:
    capture = capture_text(
        source_url=(
            "https://example.test/jobs/123?board=public&token=live-token"
            "#access_token=secret"
        ),
        text="# Public Role\n\n## Organization\nExample Labs\n",
    )

    assert capture.source_url == "https://example.test/jobs/123?board=public"
    assert "live-token" not in capture.source_url
    assert "access_token" not in capture.source_url
