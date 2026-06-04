"""Generated Markdown and CSV exports derived from canonical SQLite state."""

import sqlite3
from pathlib import Path
from typing import Any

from res2jobworks_core.commands._support import failure, slug, validate_output_path
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def export_applications(
    database_path: Path | str,
    *,
    output_path: Path | str,
    format: str,
    export_id: str | None = None,
) -> CommandEnvelope:
    """Generate a tracker export from SQLite and record it as an artifact."""
    command = "applications.export"
    inputs = {
        "database_path": str(database_path),
        "output_path": str(output_path),
        "format": format,
    }
    try:
        path = validate_output_path(output_path)
        repository = SQLiteRepository(database_path)
        applications = repository.list_applications()
        if not applications:
            raise ValueError("at least one application is required before export")
        jobs = {job["id"]: job for job in repository.list_jobs()}
        evaluations = {item["id"]: item for item in repository.list_evaluations()}
        if format == "markdown":
            content = render_markdown_tracker(applications, jobs, evaluations)
        elif format == "csv":
            content = render_csv_tracker(applications, jobs, evaluations)
        else:
            raise ValueError("export format must be markdown or csv")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        record = repository.record_export(
            export_id=export_id or f"export-{slug(str(path))}",
            export_type="application_tracker",
            format=format,
            target_table="applications",
            target_id=applications[0]["id"],
            path=path.as_posix(),
            metadata={
                "generated_by": command,
                "application_count": len(applications),
            },
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"export_record": record},
            files=[path.as_posix()],
        )
    except (OSError, RepositoryError, sqlite3.Error, ValueError) as exc:
        return failure(command, inputs, exc)


def render_markdown_tracker(
    applications: list[dict[str, Any]],
    jobs: dict[str, dict[str, Any]],
    evaluations: dict[str, dict[str, Any]],
) -> str:
    """Render a human-readable application tracker summary."""
    lines = ["# res2jobWorks Application Tracker", ""]
    for application in applications:
        job = jobs.get(application["job_id"], {})
        evaluation = evaluations.get(application.get("evaluation_id") or "", {})
        lines.extend(
            [
                f"## {job.get('title', application['job_id'])}",
                "",
                f"- Employer: {job.get('employer', 'Unknown')}",
                f"- Status: {application['current_status']}",
                f"- Evaluation score: {evaluation.get('score', 'not evaluated')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def render_csv_tracker(
    applications: list[dict[str, Any]],
    jobs: dict[str, dict[str, Any]],
    evaluations: dict[str, dict[str, Any]],
) -> str:
    """Render application tracker rows as CSV text."""
    rows = ["application_id,job_id,employer,title,status,evaluation_score"]
    for application in applications:
        job = jobs.get(application["job_id"], {})
        evaluation = evaluations.get(application.get("evaluation_id") or "", {})
        rows.append(
            ",".join(
                _csv_cell(value)
                for value in [
                    application["id"],
                    application["job_id"],
                    job.get("employer", ""),
                    job.get("title", ""),
                    application["current_status"],
                    evaluation.get("score", ""),
                ]
            )
        )
    return "\n".join(rows) + "\n"


def _csv_cell(value: object) -> str:
    text = str(value)
    if any(char in text for char in [",", "\"", "\n"]):
        escaped = text.replace('"', '""')
        return f'"{escaped}"'
    return text
