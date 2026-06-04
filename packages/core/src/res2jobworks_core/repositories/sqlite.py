"""Explicit repository APIs for the canonical SQLite data model.

The repository hides raw SQL from future clients while keeping the persistence
surface narrow, typed, and easy to inspect. Methods validate required fields and
preserve append-only status history.
"""

import json
import sqlite3
from pathlib import Path, PureWindowsPath
from typing import Any

from res2jobworks_core._privacy import REDACTED as REDACTED
from res2jobworks_core._privacy import redact_secrets as _redact_secrets
from res2jobworks_core.db.connection import connect
from res2jobworks_core.db.migrations import apply_migrations

APPLICATION_STATUSES = {
    "interested",
    "applied",
    "interviewing",
    "offer",
    "rejected",
    "withdrawn",
    "archived",
}
AGENT_RUN_STATUSES = {
    "pending",
    "running",
    "completed",
    "failed",
    "cancelled",
}


class RepositoryError(ValueError):
    """Raised when repository inputs violate core persistence invariants."""


class SQLiteRepository:
    """Persistence facade for one migrated res2jobWorks SQLite workspace."""

    def __init__(self, database_path: Path | str) -> None:
        self.database_path = database_path
        apply_migrations(database_path)

    def create_profile(
        self,
        *,
        profile_id: str,
        display_name: str,
        headline: str = "",
        summary: str = "",
        skills: list[str] | None = None,
    ) -> dict[str, Any]:
        """Persist a profile record and return the stored row."""
        _require(profile_id, "profile_id")
        _require(display_name, "display_name")
        with connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO profiles(id, display_name, headline, summary, skills_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    profile_id,
                    display_name,
                    headline,
                    summary,
                    _json(skills or []),
                ),
            )
            return self.get_profile(profile_id, connection=connection)

    def add_resume_source(
        self,
        *,
        source_id: str,
        profile_id: str,
        source_type: str,
        title: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Attach an immutable resume/profile source to a profile."""
        _require_all(
            source_id=source_id,
            profile_id=profile_id,
            source_type=source_type,
            title=title,
            content=content,
        )
        with connect(self.database_path) as connection:
            self._require_record_exists(connection, "profiles", profile_id)
            connection.execute(
                """
                INSERT INTO resume_sources(
                    id, profile_id, source_type, title, content, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    source_id,
                    profile_id,
                    source_type,
                    title,
                    content,
                    _json(metadata or {}),
                ),
            )
            return _one(
                connection,
                "SELECT * FROM resume_sources WHERE id = ?",
                source_id,
            )

    def get_profile(
        self,
        profile_id: str,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> dict[str, Any]:
        """Return a profile by id or raise a clear repository error."""
        _require(profile_id, "profile_id")
        if connection is not None:
            return _one(connection, "SELECT * FROM profiles WHERE id = ?", profile_id)
        with connect(self.database_path) as owned_connection:
            return self.get_profile(profile_id, connection=owned_connection)

    def list_profiles(self) -> list[dict[str, Any]]:
        """Return stored profiles ordered by creation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM profiles ORDER BY created_at, id",
            )

    def list_resume_sources(self, profile_id: str) -> list[dict[str, Any]]:
        """Return source records attached to one profile."""
        _require(profile_id, "profile_id")
        with connect(self.database_path) as connection:
            self._require_record_exists(connection, "profiles", profile_id)
            return _many(
                connection,
                """
                SELECT * FROM resume_sources
                WHERE profile_id = ?
                ORDER BY created_at, id
                """,
                profile_id,
            )

    def create_job(
        self,
        *,
        job_id: str,
        employer: str,
        title: str,
        description: str,
        location: str = "",
    ) -> dict[str, Any]:
        """Persist a job record and return the stored row."""
        _require_all(
            job_id=job_id,
            employer=employer,
            title=title,
            description=description,
        )
        with connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO jobs(id, employer, title, location, description)
                VALUES (?, ?, ?, ?, ?)
                """,
                (job_id, employer, title, location, description),
            )
            return self.get_job(job_id, connection=connection)

    def add_job_source(
        self,
        *,
        source_id: str,
        job_id: str,
        source_type: str,
        title: str,
        content: str,
        source_url: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Attach an immutable source record to a job."""
        _require_all(
            source_id=source_id,
            job_id=job_id,
            source_type=source_type,
            title=title,
            content=content,
        )
        with connect(self.database_path) as connection:
            self._require_record_exists(connection, "jobs", job_id)
            connection.execute(
                """
                INSERT INTO job_sources(
                    id, job_id, source_type, title, content, source_url, metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_id,
                    job_id,
                    source_type,
                    title,
                    content,
                    source_url,
                    _json(metadata or {}),
                ),
            )
            return _one(connection, "SELECT * FROM job_sources WHERE id = ?", source_id)

    def get_job(
        self,
        job_id: str,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> dict[str, Any]:
        """Return a job by id or raise a clear repository error."""
        _require(job_id, "job_id")
        if connection is not None:
            return _one(connection, "SELECT * FROM jobs WHERE id = ?", job_id)
        with connect(self.database_path) as owned_connection:
            return self.get_job(job_id, connection=owned_connection)

    def list_jobs(self) -> list[dict[str, Any]]:
        """Return stored jobs ordered by creation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM jobs ORDER BY created_at, id",
            )

    def list_job_sources(self, job_id: str) -> list[dict[str, Any]]:
        """Return source records attached to one job."""
        _require(job_id, "job_id")
        with connect(self.database_path) as connection:
            self._require_record_exists(connection, "jobs", job_id)
            return _many(
                connection,
                """
                SELECT * FROM job_sources
                WHERE job_id = ?
                ORDER BY created_at, id
                """,
                job_id,
            )

    def create_evaluation(
        self,
        *,
        evaluation_id: str,
        profile_id: str,
        job_id: str,
        rubric_version: str,
        score: int,
        summary: str,
        recommendation: str,
        citations: list[dict[str, Any]],
        provider_kind: str = "deterministic",
        provider_name: str | None = None,
        provider_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Persist an evaluation and its required citations atomically."""
        _require_all(
            evaluation_id=evaluation_id,
            profile_id=profile_id,
            job_id=job_id,
            rubric_version=rubric_version,
            summary=summary,
            recommendation=recommendation,
            provider_kind=provider_kind,
        )
        if not 0 <= score <= 100:
            msg = "score must be between 0 and 100"
            raise RepositoryError(msg)
        if not citations:
            msg = "evaluations require at least one citation"
            raise RepositoryError(msg)

        with connect(self.database_path) as connection:
            with connection:
                self._require_record_exists(connection, "profiles", profile_id)
                self._require_record_exists(connection, "jobs", job_id)
                connection.execute(
                    """
                    INSERT INTO evaluations(
                        id, profile_id, job_id, rubric_version, score, summary,
                        recommendation, provider_kind, provider_name,
                        provider_metadata_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        evaluation_id,
                        profile_id,
                        job_id,
                        rubric_version,
                        score,
                        summary,
                        recommendation,
                        provider_kind,
                        provider_name,
                        _json(_redact_secrets(provider_metadata or {})),
                    ),
                )
                for index, citation in enumerate(citations, start=1):
                    self._insert_citation(
                        connection,
                        evaluation_id,
                        profile_id,
                        job_id,
                        index,
                        citation,
                    )
            return self.get_evaluation(evaluation_id, connection=connection)

    def get_evaluation(
        self,
        evaluation_id: str,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> dict[str, Any]:
        """Return an evaluation with its citation rows."""
        _require(evaluation_id, "evaluation_id")
        if connection is None:
            with connect(self.database_path) as owned_connection:
                return self.get_evaluation(evaluation_id, connection=owned_connection)

        evaluation = _one(
            connection,
            "SELECT * FROM evaluations WHERE id = ?",
            evaluation_id,
        )
        citations = _many(
            connection,
            """
            SELECT * FROM evaluation_citations
            WHERE evaluation_id = ?
            ORDER BY id
            """,
            evaluation_id,
        )
        return {**evaluation, "citations": citations}

    def list_evaluations(self) -> list[dict[str, Any]]:
        """Return stored evaluations ordered by creation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM evaluations ORDER BY created_at, id",
            )

    def create_application(
        self,
        *,
        application_id: str,
        job_id: str,
        status: str,
        evaluation_id: str | None = None,
        note: str = "",
        event_id: str | None = None,
    ) -> dict[str, Any]:
        """Create an application and its initial append-only status event."""
        _require_all(application_id=application_id, job_id=job_id, status=status)
        _require_known_value(status, "status", APPLICATION_STATUSES)
        event_id = event_id or f"{application_id}-status-001"
        with connect(self.database_path) as connection:
            with connection:
                self._require_record_exists(connection, "jobs", job_id)
                if evaluation_id is not None:
                    self._require_evaluation_matches_job(
                        connection,
                        evaluation_id,
                        job_id,
                    )
                connection.execute(
                    """
                    INSERT INTO applications(id, job_id, evaluation_id, current_status)
                    VALUES (?, ?, ?, ?)
                    """,
                    (application_id, job_id, evaluation_id, status),
                )
                connection.execute(
                    """
                    INSERT INTO application_status_events(
                        id, application_id, status, note
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (event_id, application_id, status, note),
                )
            return self.get_application(application_id, connection=connection)

    def append_status_event(
        self,
        *,
        event_id: str,
        application_id: str,
        status: str,
        note: str = "",
    ) -> dict[str, Any]:
        """Append a status event and update only the current status pointer."""
        _require_all(event_id=event_id, application_id=application_id, status=status)
        _require_known_value(status, "status", APPLICATION_STATUSES)
        with connect(self.database_path) as connection:
            with connection:
                self._require_record_exists(
                    connection,
                    "applications",
                    application_id,
                )
                connection.execute(
                    """
                    INSERT INTO application_status_events(
                        id, application_id, status, note
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (event_id, application_id, status, note),
                )
                connection.execute(
                    """
                    UPDATE applications
                    SET current_status = ?,
                        updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                    WHERE id = ?
                    """,
                    (status, application_id),
                )
            return self.get_application(application_id, connection=connection)

    def get_application(
        self,
        application_id: str,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> dict[str, Any]:
        """Return an application with ordered status events."""
        _require(application_id, "application_id")
        if connection is None:
            with connect(self.database_path) as owned_connection:
                return self.get_application(application_id, connection=owned_connection)

        application = _one(
            connection,
            "SELECT * FROM applications WHERE id = ?",
            application_id,
        )
        events = self.list_status_events(application_id, connection=connection)
        return {**application, "status_events": events}

    def list_applications(self) -> list[dict[str, Any]]:
        """Return stored applications ordered by creation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM applications ORDER BY created_at, id",
            )

    def list_status_events(
        self,
        application_id: str,
        *,
        connection: sqlite3.Connection | None = None,
    ) -> list[dict[str, Any]]:
        """Return status events without mutating application history."""
        _require(application_id, "application_id")
        if connection is None:
            with connect(self.database_path) as owned_connection:
                return self.list_status_events(
                    application_id,
                    connection=owned_connection,
                )
        return _many(
            connection,
            """
            SELECT * FROM application_status_events
            WHERE application_id = ?
            ORDER BY created_at, id
            """,
            application_id,
        )

    def add_note(
        self,
        *,
        note_id: str,
        body: str,
        application_id: str | None = None,
        job_id: str | None = None,
        evaluation_id: str | None = None,
    ) -> dict[str, Any]:
        """Attach a note to at least one canonical record."""
        _require_all(note_id=note_id, body=body)
        if not any([application_id, job_id, evaluation_id]):
            msg = "note must reference an application, job, or evaluation"
            raise RepositoryError(msg)
        with connect(self.database_path) as connection:
            if application_id is not None:
                self._require_record_exists(connection, "applications", application_id)
            if job_id is not None:
                self._require_record_exists(connection, "jobs", job_id)
            if evaluation_id is not None:
                self._require_record_exists(connection, "evaluations", evaluation_id)
            connection.execute(
                """
                INSERT INTO notes(id, application_id, job_id, evaluation_id, body)
                VALUES (?, ?, ?, ?, ?)
                """,
                (note_id, application_id, job_id, evaluation_id, body),
            )
            return _one(connection, "SELECT * FROM notes WHERE id = ?", note_id)

    def record_export(
        self,
        *,
        export_id: str,
        export_type: str,
        format: str,
        target_table: str,
        target_id: str,
        path: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Record a generated export artifact that points at canonical state."""
        _require_all(
            export_id=export_id,
            export_type=export_type,
            format=format,
            target_table=target_table,
            target_id=target_id,
            path=path,
        )
        if format not in {"markdown", "csv", "json", "pdf", "docx"}:
            msg = "export format must be markdown, csv, json, pdf, or docx"
            raise RepositoryError(msg)
        _validate_artifact_path(path)
        self._require_target_exists(target_table, target_id)
        with connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO exports(
                    id, export_type, format, target_table, target_id, path,
                    metadata_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    export_id,
                    export_type,
                    format,
                    target_table,
                    target_id,
                    path,
                    _json(_redact_secrets(metadata or {})),
                ),
            )
            return _one(connection, "SELECT * FROM exports WHERE id = ?", export_id)

    def list_exports(self) -> list[dict[str, Any]]:
        """Return generated export records ordered by generation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM exports ORDER BY generated_at, id",
            )

    def record_agent_run(
        self,
        *,
        run_id: str,
        command_id: str,
        status: str,
        provider: str = "local",
        input: dict[str, Any] | None = None,
        output: dict[str, Any] | None = None,
        evaluation_id: str | None = None,
        application_id: str | None = None,
    ) -> dict[str, Any]:
        """Record an agent/client run without storing secrets or credentials."""
        _require_all(
            run_id=run_id,
            command_id=command_id,
            status=status,
            provider=provider,
        )
        _require_known_value(status, "status", AGENT_RUN_STATUSES)
        with connect(self.database_path) as connection:
            if evaluation_id is not None:
                self._require_record_exists(connection, "evaluations", evaluation_id)
            if application_id is not None:
                self._require_record_exists(connection, "applications", application_id)
            connection.execute(
                """
                INSERT INTO agent_runs(
                    id, command_id, provider, status, input_json, output_json,
                    evaluation_id, application_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    command_id,
                    provider,
                    status,
                    _json(_redact_secrets(input or {})),
                    _json(_redact_secrets(output or {})),
                    evaluation_id,
                    application_id,
                ),
            )
            return _one(connection, "SELECT * FROM agent_runs WHERE id = ?", run_id)

    def list_agent_runs(self) -> list[dict[str, Any]]:
        """Return stored agent run metadata ordered by creation time and id."""
        with connect(self.database_path) as connection:
            return _many(
                connection,
                "SELECT * FROM agent_runs ORDER BY created_at, id",
            )

    def _insert_citation(
        self,
        connection: sqlite3.Connection,
        evaluation_id: str,
        profile_id: str,
        job_id: str,
        index: int,
        citation: dict[str, Any],
    ) -> None:
        source_table = str(citation.get("source_table", ""))
        source_id = str(citation.get("source_id", ""))
        quote = str(citation.get("quote", ""))
        _require_all(source_table=source_table, source_id=source_id, quote=quote)
        if source_table not in {"resume_sources", "job_sources"}:
            msg = "citation source_table must be resume_sources or job_sources"
            raise RepositoryError(msg)
        self._require_citation_source_matches_evaluation(
            connection,
            source_table,
            source_id,
            profile_id,
            job_id,
        )
        connection.execute(
            """
            INSERT INTO evaluation_citations(
                id, evaluation_id, source_table, source_id, quote, start_offset,
                end_offset, rationale
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(citation.get("id") or f"{evaluation_id}-citation-{index:03d}"),
                evaluation_id,
                source_table,
                source_id,
                quote,
                citation.get("start_offset"),
                citation.get("end_offset"),
                str(citation.get("rationale", "")),
            ),
        )

    def _require_citation_source_matches_evaluation(
        self,
        connection: sqlite3.Connection,
        source_table: str,
        source_id: str,
        profile_id: str,
        job_id: str,
    ) -> None:
        if source_table == "resume_sources":
            row = connection.execute(
                "SELECT profile_id FROM resume_sources WHERE id = ?",
                (source_id,),
            ).fetchone()
            if row is None:
                msg = f"citation source does not exist: {source_table}:{source_id}"
                raise RepositoryError(msg)
            if row["profile_id"] != profile_id:
                msg = "citation resume source must belong to the evaluation profile"
                raise RepositoryError(msg)
            return

        row = connection.execute(
            "SELECT job_id FROM job_sources WHERE id = ?",
            (source_id,),
        ).fetchone()
        if row is None:
            msg = f"citation source does not exist: {source_table}:{source_id}"
            raise RepositoryError(msg)
        if row["job_id"] != job_id:
            msg = "citation job source must belong to the evaluation job"
            raise RepositoryError(msg)

    def _require_record_exists(
        self,
        connection: sqlite3.Connection,
        table: str,
        record_id: str,
    ) -> None:
        allowed_tables = {
            "applications",
            "evaluations",
            "jobs",
            "profiles",
        }
        if table not in allowed_tables:
            msg = f"unsupported lookup table: {table}"
            raise RepositoryError(msg)
        row = connection.execute(
            f"SELECT id FROM {table} WHERE id = ?",
            (record_id,),
        ).fetchone()
        if row is None:
            msg = f"{table.removesuffix('s')} does not exist: {record_id}"
            raise RepositoryError(msg)

    def _require_evaluation_matches_job(
        self,
        connection: sqlite3.Connection,
        evaluation_id: str,
        job_id: str,
    ) -> None:
        row = connection.execute(
            "SELECT job_id FROM evaluations WHERE id = ?",
            (evaluation_id,),
        ).fetchone()
        if row is None:
            msg = f"evaluation does not exist: {evaluation_id}"
            raise RepositoryError(msg)
        if row["job_id"] != job_id:
            msg = "application evaluation must belong to the same job"
            raise RepositoryError(msg)

    def _require_target_exists(self, target_table: str, target_id: str) -> None:
        allowed_tables = {"applications", "evaluations", "jobs", "profiles"}
        if target_table not in allowed_tables:
            msg = f"unsupported export target table: {target_table}"
            raise RepositoryError(msg)
        with connect(self.database_path) as connection:
            row = connection.execute(
                f"SELECT id FROM {target_table} WHERE id = ?",
                (target_id,),
            ).fetchone()
        if row is None:
            msg = f"export target does not exist: {target_table}:{target_id}"
            raise RepositoryError(msg)


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def _validate_artifact_path(path: str) -> None:
    artifact_path = Path(path)
    windows_path = PureWindowsPath(path)
    if (
        artifact_path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
        or ".." in artifact_path.parts
        or ".." in windows_path.parts
    ):
        msg = "export path must be relative and stay inside the workspace"
        raise RepositoryError(msg)


def _require(value: str, field: str) -> None:
    if not value or not str(value).strip():
        msg = f"{field} is required"
        raise RepositoryError(msg)


def _require_all(**values: str) -> None:
    for field, value in values.items():
        _require(value, field)


def _require_known_value(value: str, field: str, allowed_values: set[str]) -> None:
    if value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        msg = f"{field} must be one of: {allowed}"
        raise RepositoryError(msg)


def _one(connection: sqlite3.Connection, query: str, *params: object) -> dict[str, Any]:
    row = connection.execute(query, params).fetchone()
    if row is None:
        msg = "record not found"
        raise RepositoryError(msg)
    return _decode_row(row)


def _many(
    connection: sqlite3.Connection,
    query: str,
    *params: object,
) -> list[dict[str, Any]]:
    return [_decode_row(row) for row in connection.execute(query, params).fetchall()]


def _decode_row(row: sqlite3.Row) -> dict[str, Any]:
    decoded = dict(row)
    for key in list(decoded):
        if key.endswith("_json"):
            decoded[key.removesuffix("_json")] = json.loads(decoded.pop(key))
    return decoded
