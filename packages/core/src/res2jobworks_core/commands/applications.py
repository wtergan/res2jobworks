"""Application tracking workflows over append-only status history."""

import sqlite3
from pathlib import Path

from res2jobworks_core.commands._support import failure
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def add_application(
    database_path: Path | str,
    *,
    job_id: str,
    status: str = "interested",
    application_id: str | None = None,
    evaluation_id: str | None = None,
    note: str = "",
) -> CommandEnvelope:
    """Create an application tracking record for a stored job."""
    command = "applications.add"
    inputs = {"database_path": str(database_path), "job_id": job_id, "status": status}
    try:
        resolved_application_id = application_id or f"application-{job_id}"
        application = SQLiteRepository(database_path).create_application(
            application_id=resolved_application_id,
            job_id=job_id,
            status=status,
            evaluation_id=evaluation_id,
            note=note,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={
                "application": application,
                "status_event": application["status_events"][-1],
            },
        )
    except (RepositoryError, sqlite3.Error) as exc:
        return failure(command, inputs, exc)


def update_application(
    database_path: Path | str,
    *,
    application_id: str,
    status: str,
    note: str = "",
    event_id: str | None = None,
) -> CommandEnvelope:
    """Append an application status event without rewriting history."""
    command = "applications.update"
    inputs = {
        "database_path": str(database_path),
        "application_id": application_id,
        "status": status,
    }
    try:
        repository = SQLiteRepository(database_path)
        existing_count = len(repository.list_status_events(application_id))
        resolved_event_id = (
            event_id or f"{application_id}-status-{existing_count + 1:03d}"
        )
        application = repository.append_status_event(
            event_id=resolved_event_id,
            application_id=application_id,
            status=status,
            note=note,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={
                "application": application,
                "status_event": application["status_events"][-1],
            },
        )
    except (RepositoryError, sqlite3.Error) as exc:
        return failure(command, inputs, exc)


def list_applications(database_path: Path | str) -> CommandEnvelope:
    """List application tracker records from canonical state."""
    command = "applications.list"
    inputs = {"database_path": str(database_path)}
    try:
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"applications": SQLiteRepository(database_path).list_applications()},
        )
    except (RepositoryError, sqlite3.Error) as exc:
        return failure(command, inputs, exc)
