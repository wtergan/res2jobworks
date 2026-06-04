"""Safety helpers for browser automation evidence and review payloads.

Automation inputs can originate from browser pages, forms, and local capture
artifacts. This module keeps those client-side values portable and prevents
credential-like material from entering command envelopes or SQLite metadata.
"""

from __future__ import annotations

import re
from pathlib import Path, PureWindowsPath
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ANSI_ESCAPE_RE = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\].*?(?:\x07|\x1b\\))")
CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x1f\x7f-\x9f]")

REVIEW_STATE_LABELS = {
    "captured_for_human_review": "Captured for human review",
    "human_review_required": "Needs human review before use",
}

SENSITIVE_QUERY_PARTS = {
    "access_token",
    "api_key",
    "auth",
    "authorization",
    "client_secret",
    "code",
    "cookie",
    "credential",
    "id_token",
    "key",
    "password",
    "refresh_token",
    "secret",
    "session",
    "signature",
    "token",
}

SENSITIVE_FIELD_PARTS = {
    "access_token",
    "api_key",
    "authorization",
    "client_secret",
    "cookie",
    "credential",
    "id_token",
    "otp",
    "passcode",
    "password",
    "refresh_token",
    "secret",
    "session",
    "token",
}


def sanitize_source_url(source_url: str) -> str:
    """Return a URL safe to persist and render as source evidence."""
    cleaned = strip_control_characters(source_url).strip()
    if not cleaned:
        raise ValueError("source_url is required")
    parsed = urlsplit(cleaned)
    if parsed.username or parsed.password:
        raise ValueError("source_url cannot include userinfo credentials")
    safe_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not is_sensitive_query_key(key)
    ]
    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(safe_query, doseq=True),
            "",
        )
    )


def validate_evidence_path(path: str) -> str:
    """Return a portable relative artifact path or raise a validation error."""
    cleaned = strip_control_characters(path).strip()
    artifact_path = Path(cleaned)
    windows_path = PureWindowsPath(cleaned)
    if (
        not cleaned
        or artifact_path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or ".." in artifact_path.parts
        or ".." in windows_path.parts
    ):
        raise ValueError(
            "evidence paths must be relative and stay inside the workspace"
        )
    return cleaned


def validate_fill_fields(fields: dict[str, str]) -> dict[str, str]:
    """Return fill fields only when they do not look credential-bearing."""
    sanitized: dict[str, str] = {}
    for key, value in fields.items():
        field_name = strip_control_characters(str(key)).strip()
        if not field_name:
            raise ValueError("fill field names cannot be empty")
        if is_sensitive_field_name(field_name):
            raise ValueError(
                f"fill field cannot include credential-like name: {field_name}"
            )
        sanitized[field_name] = strip_control_characters(str(value))
    return sanitized


def review_state_label(review_state: str | None) -> str:
    """Return readable review-state text for human-facing UI surfaces."""
    if not review_state:
        return ""
    return REVIEW_STATE_LABELS.get(review_state, review_state.replace("_", " ").title())


def strip_control_characters(value: str) -> str:
    """Remove terminal/browser control characters from displayable text."""
    without_ansi = ANSI_ESCAPE_RE.sub("", value)
    return CONTROL_CHARACTER_RE.sub("", without_ansi)


def is_sensitive_query_key(key: str) -> bool:
    """Return whether a URL query key commonly carries session material."""
    normalized = normalize_name(key)
    return any(part in normalized for part in SENSITIVE_QUERY_PARTS)


def is_sensitive_field_name(key: str) -> bool:
    """Return whether a fill field name looks credential-bearing."""
    normalized = normalize_name(key)
    return any(part in normalized for part in SENSITIVE_FIELD_PARTS)


def normalize_name(key: str) -> str:
    """Normalize browser field/query names for privacy checks."""
    separated = key.replace("-", "_").replace(" ", "_")
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", separated).lower()
