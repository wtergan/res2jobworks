"""Safe browser/source automation helpers for res2jobWorks MVP 1.

Automation remains a client over core command envelopes. The package can import
captured job text and prepare fill-review plans, but it deliberately exposes no
application submission behavior.
"""

from res2jobworks_automation.capture import (
    BrowserCapture,
    CapturedJobSource,
    CaptureRequest,
    FixtureCaptureAdapter,
    SourceCaptureAdapter,
    capture_job,
    capture_text,
    import_captured_job,
)
from res2jobworks_automation.review import (
    FillDraft,
    prepare_fill_review,
)
from res2jobworks_automation.safety import (
    review_state_label,
    sanitize_source_url,
    strip_control_characters,
    validate_evidence_path,
    validate_fill_fields,
)

__all__ = [
    "BrowserCapture",
    "CapturedJobSource",
    "CaptureRequest",
    "FillDraft",
    "FixtureCaptureAdapter",
    "SourceCaptureAdapter",
    "capture_job",
    "capture_text",
    "import_captured_job",
    "prepare_fill_review",
    "review_state_label",
    "sanitize_source_url",
    "strip_control_characters",
    "validate_evidence_path",
    "validate_fill_fields",
]
