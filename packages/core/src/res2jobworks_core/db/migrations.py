"""Deterministic migration runner for local SQLite workspaces.

Migrations are packaged with the core module so installed clients and generated
wrappers can initialize the same canonical schema without depending on a source
checkout.
"""

import sqlite3
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from res2jobworks_core.db.connection import connect


@dataclass(frozen=True)
class Migration:
    """One ordered SQL migration bundled with the core package."""

    version: int
    name: str
    resource: str


MIGRATIONS: tuple[Migration, ...] = (
    Migration(
        version=1,
        name="initial_evaluation_tracking_schema",
        resource="001_initial.sql",
    ),
)


def apply_migrations(database_path: Path | str) -> int:
    """Apply all pending migrations and return the resulting schema version."""
    with connect(database_path) as connection:
        _ensure_migration_table(connection)
        applied = {
            row["version"]
            for row in connection.execute("SELECT version FROM schema_migrations")
        }
        for migration in MIGRATIONS:
            if migration.version in applied:
                continue
            sql = _read_migration_sql(migration.resource)
            with connection:
                connection.executescript(sql)
                connection.execute(
                    """
                    INSERT INTO schema_migrations(version, name)
                    VALUES (?, ?)
                    """,
                    (migration.version, migration.name),
                )
        return current_version(connection)


def current_version(connection_or_path: sqlite3.Connection | Path | str) -> int:
    """Return the latest applied schema version for a connection or database."""
    if isinstance(connection_or_path, sqlite3.Connection):
        _ensure_migration_table(connection_or_path)
        row = connection_or_path.execute(
            "SELECT COALESCE(MAX(version), 0) AS version FROM schema_migrations"
        ).fetchone()
        return int(row["version"])

    with connect(connection_or_path) as connection:
        return current_version(connection)


def table_names(database_path: Path | str) -> set[str]:
    """Return user-defined table names in a migrated workspace database."""
    with connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            """
        ).fetchall()
    return {str(row["name"]) for row in rows}


def _ensure_migration_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
        )
        """
    )


def _read_migration_sql(resource_name: str) -> str:
    return (
        resources.files("res2jobworks_core.db")
        .joinpath("migrations", resource_name)
        .read_text(encoding="utf-8")
    )
