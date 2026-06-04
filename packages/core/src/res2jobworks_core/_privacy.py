"""Internal privacy helpers for persistence and provider metadata boundaries.

The core stores provider metadata, export metadata, and agent run payloads as
canonical SQLite state. Secret-bearing keys must be redacted before those
payloads cross into durable local storage.
"""

import re
from typing import Any

REDACTED = "[REDACTED]"

SECRET_KEYS = {
    "api_key",
    "apikey",
    "authorization",
    "client_secret",
    "credential",
    "credential_blob",
    "cookie",
    "id_token",
    "password",
    "refresh_token",
    "secret",
    "session",
    "session_id",
    "sessionid",
    "token",
    "access_token",
}


def redact_secrets(value: Any) -> Any:
    """Return `value` with known secret-bearing dictionary keys redacted."""
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, nested in value.items():
            if _is_secret_key(str(key)):
                redacted[key] = REDACTED
            else:
                redacted[key] = redact_secrets(nested)
        return redacted
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    return value


def _is_secret_key(key: str) -> bool:
    normalized = _normalize_key(key)
    if normalized in SECRET_KEYS:
        return True
    if normalized.startswith(("credential_", "session_")):
        return True
    if "credential" in normalized:
        return True
    return normalized.endswith(
        (
            "_access_token",
            "_api_key",
            "_client_secret",
            "_cookie",
            "_credential",
            "_id_token",
            "_password",
            "_refresh_token",
            "_secret",
            "_session",
            "_session_id",
            "_sessionid",
            "_token",
        )
    )


def _normalize_key(key: str) -> str:
    separated = key.replace("-", "_").replace(" ", "_")
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", separated).lower()
