"""Shared dashboard read model for thin local app clients.

This module coordinates read-only core command envelopes for TUI and web
surfaces. It does not own product rules or persistence; it only keeps client
presentation code from duplicating the same `jobs.list` plus `jobs.show`
orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from res2jobworks_core.commands import list_jobs, show_job
from res2jobworks_core.contracts import CommandEnvelope


@dataclass(frozen=True)
class DashboardJob:
    """One listed job paired with its detail command envelope."""

    summary: dict[str, Any]
    detail: CommandEnvelope


def load_dashboard_jobs(
    database_path: Path | str,
) -> tuple[CommandEnvelope, list[DashboardJob]]:
    """Load job summaries and per-job detail envelopes for dashboard clients."""
    jobs_envelope = list_jobs(database_path)
    if not jobs_envelope.ok:
        return jobs_envelope, []

    jobs = [
        DashboardJob(
            summary=job,
            detail=show_job(database_path, job_id=job["id"]),
        )
        for job in jobs_envelope.data["jobs"]
    ]
    return jobs_envelope, jobs
