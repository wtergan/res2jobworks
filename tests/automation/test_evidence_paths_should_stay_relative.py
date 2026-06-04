import pytest

from res2jobworks_automation import capture_text


def test_evidence_paths_should_stay_relative() -> None:
    with pytest.raises(ValueError, match="evidence paths must be relative"):
        capture_text(
            source_url="https://example.test/jobs/123",
            text="# Public Role\n\n## Organization\nExample Labs\n",
            artifact_paths=("/home/example/.config/browser/Cookies",),
        )
