"""Command-envelope wrappers for phase 2 document workflows."""

from __future__ import annotations

from pathlib import Path

from res2jobworks_core.commands._support import failure
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError
from res2jobworks_documents.drafting import (
    build_application_answer_draft,
    build_cover_letter_draft,
    build_tailoring_suggestions,
)
from res2jobworks_documents.renderers import render_document_artifact


def suggest_tailoring(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None = None,
) -> CommandEnvelope:
    """Return evidence-backed tailoring suggestions for human review."""
    command = "documents.suggest_tailoring"
    inputs = _inputs(database_path, profile_id, job_id, evaluation_id)
    try:
        suggestions = build_tailoring_suggestions(
            database_path,
            profile_id=profile_id,
            job_id=job_id,
            evaluation_id=evaluation_id,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"suggestions": suggestions},
            warnings=["tailoring suggestions require human review before use"],
        )
    except (RepositoryError, ValueError) as exc:
        return failure(command, inputs, exc)


def draft_cover_letter(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None = None,
    requested_focus: tuple[str, ...] = (),
) -> CommandEnvelope:
    """Return a cited cover letter draft without rendering or submission."""
    command = "documents.draft_cover_letter"
    inputs = {
        **_inputs(database_path, profile_id, job_id, evaluation_id),
        "requested_focus": list(requested_focus),
    }
    try:
        draft = build_cover_letter_draft(
            database_path,
            profile_id=profile_id,
            job_id=job_id,
            evaluation_id=evaluation_id,
            requested_focus=requested_focus,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"draft": draft.to_dict()},
            warnings=["draft requires human review before use"],
        )
    except (RepositoryError, ValueError) as exc:
        return failure(command, inputs, exc)


def draft_application_answer(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    question: str,
    evaluation_id: str | None = None,
) -> CommandEnvelope:
    """Return a cited application-answer draft without rendering or submission."""
    command = "documents.draft_application_answer"
    inputs = {
        **_inputs(database_path, profile_id, job_id, evaluation_id),
        "question": question,
    }
    try:
        draft = build_application_answer_draft(
            database_path,
            profile_id=profile_id,
            job_id=job_id,
            question=question,
            evaluation_id=evaluation_id,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"draft": draft.to_dict()},
            warnings=["draft requires human review before use"],
        )
    except (RepositoryError, ValueError) as exc:
        return failure(command, inputs, exc)


def render_cover_letter(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    output_path: Path | str,
    format: str = "markdown",
    evaluation_id: str | None = None,
) -> CommandEnvelope:
    """Render a cover letter artifact and record export metadata."""
    command = "documents.render_cover_letter"
    inputs = {
        **_inputs(database_path, profile_id, job_id, evaluation_id),
        "format": format,
        "output_path": str(output_path),
    }
    try:
        draft = build_cover_letter_draft(
            database_path,
            profile_id=profile_id,
            job_id=job_id,
            evaluation_id=evaluation_id,
        )
        export_record = render_document_artifact(
            database_path,
            draft=draft,
            output_path=output_path,
            format=format,
            target_table="jobs",
            target_id=job_id,
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"draft": draft.to_dict(), "export_record": export_record},
            files=[str(output_path)],
            warnings=["generated document artifact requires human review"],
        )
    except (RepositoryError, ValueError) as exc:
        return failure(command, inputs, exc)


def _inputs(
    database_path: Path | str,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None,
) -> dict:
    return {
        "database_path": str(database_path),
        "profile_id": profile_id,
        "job_id": job_id,
        "evaluation_id": evaluation_id,
    }
