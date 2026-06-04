"""SQLite connection helpers with core workspace invariants."""

import sqlite3
from pathlib import Path


def connect(database_path: Path | str) -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys and row mapping enabled."""
    if str(database_path) != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(database_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
