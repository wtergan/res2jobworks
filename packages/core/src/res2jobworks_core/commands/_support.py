"""Shared command helpers for input validation and envelope failures."""

from collections.abc import Iterable
from pathlib import Path, PureWindowsPath
from typing import Any

from res2jobworks_core.contracts import CommandEnvelope, CommandError
from res2jobworks_core.fixtures import validate_public_fixture_text


def read_source(
    *,
    source_path: Path | str | None,
    source_text: str | None,
) -> tuple[str, str]:
    """Read exactly one source path or inline source text."""
    if source_text is not None:
        return "inline", source_text
    if source_path is None:
        raise ValueError("source_path or source_text is required")
    path = Path(source_path)
    return path.name, path.read_text(encoding="utf-8")


def validate_public_text(text: str, source_type: str, label: str) -> None:
    """Validate public-generic content only for fixture-labeled imports."""
    if not is_fixture_source(source_type):
        return
    result = validate_public_fixture_text(text)
    if not result.ok:
        raise ValueError(f"{label} is not public-generic: {', '.join(result.errors)}")


def is_fixture_source(source_type: str) -> bool:
    """Return whether a source type must satisfy public fixture rules."""
    return source_type == "fixture" or source_type.endswith("_fixture")


def validate_output_path(output_path: Path | str) -> Path:
    """Return a relative export path or raise a portable validation error."""
    path = Path(output_path)
    windows_path = PureWindowsPath(str(output_path))
    if path.is_absolute() or windows_path.is_absolute() or windows_path.drive:
        raise ValueError("output_path must be relative")
    if ".." in path.parts or ".." in windows_path.parts:
        raise ValueError("output_path must stay inside the workspace")
    return path


def first_markdown_heading(text: str) -> str | None:
    """Return the first level-one Markdown heading from text."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return None


def extract_markdown_field(text: str, heading: str) -> str | None:
    """Return the first non-empty line after a level-two Markdown heading."""
    lines = text.splitlines()
    marker = f"## {heading}"
    for index, line in enumerate(lines):
        if line.strip() != marker:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if stripped:
                return stripped
    return None


def first_matching_line(text: str, matches: Iterable[str]) -> str:
    """Return a non-empty source line, preferring lines containing matches."""
    lowered_matches = [match.lower() for match in matches]
    for line in text.splitlines():
        stripped = line.strip(" -")
        if stripped and any(match in stripped.lower() for match in lowered_matches):
            return stripped
    for line in text.splitlines():
        stripped = line.strip(" -")
        if stripped:
            return stripped
    raise ValueError("citation source must contain non-empty text")


def organization_name(value: str) -> str:
    """Trim fixture prose down to the organization name when possible."""
    normalized = value.strip()
    if " is " in normalized:
        return normalized.split(" is ", 1)[0].strip()
    return normalized


def required_text(raw: dict[str, Any], key: str) -> str:
    """Return a required string field from parsed input data."""
    value = str(raw.get(key, "")).strip()
    if not value:
        raise ValueError(f"profile field is required: {key}")
    return value


def slug(value: str) -> str:
    """Return a stable lowercase id slug for visible command labels."""
    normalized = [
        char.lower() if char.isalnum() else "-"
        for char in value.strip()
    ]
    result = "-".join(part for part in "".join(normalized).split("-") if part)
    return result or "item"


def failure(
    command: str,
    inputs: dict[str, Any],
    exc: Exception,
) -> CommandEnvelope:
    """Build a failed command envelope from a caught exception."""
    return CommandEnvelope.failure(
        command,
        inputs=inputs,
        errors=[
            CommandError(
                code=exc.__class__.__name__,
                message=str(exc),
            )
        ],
    )
