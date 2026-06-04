"""Capture browser-visible job text and import it through core workflows.

This module owns only safe source-capture contracts. It does not hold browser
sessions, cookies, credentials, or submit actions; captured text is adapted into
the core `jobs.import` workflow so SQLite remains the canonical store.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

from res2jobworks_automation.safety import (
    sanitize_source_url,
    validate_evidence_path,
)
from res2jobworks_core.commands import import_job
from res2jobworks_core.contracts import CommandEnvelope

AUTOMATION_CAPTURE_COMMAND = "automation.capture_job"


@dataclass(frozen=True)
class BrowserCapture:
    """One reviewed browser/source capture safe to feed into core import."""

    source_url: str
    text: str
    captured_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    artifact_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class CapturedJobSource:
    """Reviewed browser job source with evidence metadata for SQLite import."""

    source_url: str
    title: str
    text: str
    captured_at: datetime
    screenshot_path: str | None = None
    artifact_paths: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CaptureRequest:
    """Request object for fake/local source capture adapters."""

    source_url: str


class SourceCaptureAdapter(Protocol):
    """Adapter contract for browser, fixture, or local capture implementations."""

    def capture(self, request: CaptureRequest) -> CapturedJobSource:
        """Return reviewed visible job text without storing browser state."""


@dataclass(frozen=True)
class FixtureCaptureAdapter:
    """In-memory adapter for tests and local fixtures without browser dependency."""

    captures: Mapping[str, CapturedJobSource]

    def capture(self, request: CaptureRequest) -> CapturedJobSource:
        """Return a configured capture for the requested source URL."""
        try:
            return self.captures[request.source_url]
        except KeyError as exc:
            msg = f"no fixture capture for source_url: {request.source_url}"
            raise ValueError(msg) from exc


def capture_text(
    *,
    source_url: str,
    text: str,
    captured_at: str | None = None,
    artifact_paths: tuple[str, ...] = (),
) -> BrowserCapture:
    """Build a sanitized capture object from visible source text."""
    if not text.strip():
        raise ValueError("captured text is required")
    return BrowserCapture(
        source_url=sanitize_source_url(source_url),
        text=text,
        captured_at=captured_at or datetime.now(UTC).isoformat(),
        artifact_paths=tuple(validate_evidence_path(path) for path in artifact_paths),
    )


def import_captured_job(
    database_path: Path | str,
    captured: CapturedJobSource,
    *,
    job_id: str | None = None,
    source_type: str = "browser_capture",
) -> CommandEnvelope:
    """Import captured browser evidence through the core job import command."""
    source_url = sanitize_source_url(captured.source_url)
    artifact_paths = [
        validate_evidence_path(path) for path in captured.artifact_paths
    ]
    source_metadata = {
        "artifact_paths": artifact_paths,
        "captured_at": captured.captured_at.isoformat(),
        "evidence_kind": "browser_capture",
        "imported_by": AUTOMATION_CAPTURE_COMMAND,
        "source_title": captured.title,
    }
    if captured.screenshot_path:
        source_metadata["screenshot_path"] = validate_evidence_path(
            captured.screenshot_path
        )
    core_envelope = import_job(
        database_path,
        source_text=captured.text,
        source_type=source_type,
        job_id=job_id,
        source_url=source_url,
        source_metadata=source_metadata,
    )
    inputs = {
        "database_path": str(database_path),
        "job_id": job_id,
        "source_type": source_type,
        "source_url": source_url,
    }
    if not core_envelope.ok:
        return CommandEnvelope.failure(
            AUTOMATION_CAPTURE_COMMAND,
            inputs=inputs,
            data={"core_envelope": core_envelope.model_dump(mode="json")},
            errors=core_envelope.errors,
            warnings=core_envelope.warnings,
        )
    return CommandEnvelope.success(
        AUTOMATION_CAPTURE_COMMAND,
        inputs=inputs,
        data={
            **core_envelope.data,
            "capture": {
                "source_url": source_url,
                "captured_at": captured.captured_at.isoformat(),
                "artifact_paths": artifact_paths,
                "screenshot_path": source_metadata.get("screenshot_path"),
            },
            "core_envelope": core_envelope.model_dump(mode="json"),
        },
        warnings=core_envelope.warnings,
    )


def capture_job(
    database_path: Path | str,
    *,
    capture: BrowserCapture,
    source_type: str = "browser_capture",
) -> CommandEnvelope:
    """Import a reviewed browser capture through the core job import workflow."""
    envelope = import_job(
        database_path,
        source_text=capture.text,
        source_type=source_type,
        source_url=capture.source_url,
        source_metadata={
            "captured_at": capture.captured_at,
            "artifact_paths": list(capture.artifact_paths),
            "review_state": "captured_for_human_review",
        },
    )
    if not envelope.ok:
        return envelope
    return CommandEnvelope.success(
        AUTOMATION_CAPTURE_COMMAND,
        inputs={
            "database_path": str(database_path),
            "source_url": capture.source_url,
            "source_type": source_type,
        },
        data={
            "capture": {
                "source_url": capture.source_url,
                "captured_at": capture.captured_at,
                "artifact_paths": list(capture.artifact_paths),
            },
            **envelope.data,
        },
        warnings=envelope.warnings,
    )
