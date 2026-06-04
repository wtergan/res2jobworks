"""Workspace initialization workflow over SQLite migrations."""

from pathlib import Path

from res2jobworks_core.commands._support import failure
from res2jobworks_core.config import Res2JobWorksConfig
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def init_workspace(workspace_path: Path | str) -> CommandEnvelope:
    """Initialize a local workspace directory and migrated SQLite database."""
    command = "workspace.init"
    inputs = {"workspace_path": str(workspace_path)}
    try:
        workspace = Path(workspace_path)
        config = Res2JobWorksConfig()
        workspace.mkdir(parents=True, exist_ok=True)
        database_path = workspace / config.database_path
        exports_dir = workspace / config.exports_dir
        exports_dir.mkdir(parents=True, exist_ok=True)
        SQLiteRepository(database_path)
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={
                "workspace_metadata": {
                    "workspace_path": str(workspace),
                    "database_path": str(database_path),
                    "exports_dir": str(exports_dir),
                },
            },
        )
    except (OSError, RepositoryError, ValueError) as exc:
        return failure(command, inputs, exc)
