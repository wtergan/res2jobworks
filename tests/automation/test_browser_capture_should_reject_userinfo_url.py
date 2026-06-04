import pytest

from res2jobworks_automation import capture_text


def test_browser_capture_should_reject_userinfo_url() -> None:
    with pytest.raises(ValueError, match="userinfo"):
        capture_text(
            source_url="https://user:password@example.test/jobs/123",
            text="# Public Role\n\n## Organization\nExample Labs\n",
        )
