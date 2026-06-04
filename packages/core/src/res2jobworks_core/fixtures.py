"""Validation helpers for public-generic fixtures.

The checks here are intentionally conservative. They guard against common local
paths, secrets, session material, and project-private markers entering public
examples.
"""

import re
from dataclasses import dataclass
from pathlib import Path

PRIVATE_MARKERS = (
    "gilgames",
    "/home/",
    "C:\\Users\\",
    "c:/users/",
    "/Users/",
    "api_key",
    "apikey",
    "api-key",
    "secret",
    "client_secret",
    "client_id",
    "token:",
    "access_token",
    "refresh_token",
    "id_token",
    "password",
    "authorization:",
    "bearer ",
    "cookie:",
    "set-cookie:",
    "sessionid",
    "session_id",
    "oauth",
    "gho_",
    "github_pat_",
    "sk-",
    "xoxb-",
    "-----begin",
    "private resume",
)

FIXTURE_LABEL_PATTERN = re.compile(r"\b(fictional|fixture|example)\b", re.I)


@dataclass(frozen=True)
class FixtureValidationResult:
    """Result of scanning fixture text for public-safety requirements."""

    ok: bool
    errors: tuple[str, ...]


def validate_public_fixture_text(text: str) -> FixtureValidationResult:
    """Return validation errors for fixture text that is not public-generic."""
    errors: list[str] = []
    lowered = text.lower()
    for marker in PRIVATE_MARKERS:
        if marker.lower() in lowered:
            errors.append(f"fixture contains private marker: {marker}")
    if not FIXTURE_LABEL_PATTERN.search(text):
        errors.append("fixture must be labeled as fictional, fixture, or example")
    return FixtureValidationResult(ok=not errors, errors=tuple(errors))


def validate_public_fixture_files(paths: list[Path]) -> FixtureValidationResult:
    """Validate multiple fixture files and include file paths in failures."""
    errors: list[str] = []
    for path in paths:
        result = validate_public_fixture_text(path.read_text(encoding="utf-8"))
        errors.extend(f"{path}: {error}" for error in result.errors)
    return FixtureValidationResult(ok=not errors, errors=tuple(errors))


def discover_public_fixture_files(roots: list[Path]) -> list[Path]:
    """Return text fixture files under roots that should pass privacy checks."""
    suffixes = {".csv", ".json", ".md", ".txt", ".yaml", ".yml"}
    discovered: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix.lower() in suffixes:
            discovered.append(root)
            continue
        if not root.exists():
            continue
        discovered.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in suffixes
        )
    return sorted(discovered)
