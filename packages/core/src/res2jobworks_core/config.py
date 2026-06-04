"""Local configuration defaults for the res2jobWorks core.

The bootstrap configuration is intentionally small and local-first. Defaults use
relative project paths, keep provider credentials out of config, and avoid
machine-specific home-directory assumptions so public examples stay portable.
"""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Res2JobWorksConfig(BaseModel):
    """Portable local defaults for a res2jobWorks workspace."""

    workspace_dir: Path = Field(default=Path(".res2jobworks"))
    data_dir: Path = Field(default=Path(".res2jobworks/data"))
    exports_dir: Path = Field(default=Path("exports"))
    default_registry_path: Path = Field(default=Path("commands/registry.yaml"))
    enable_provider_calls: bool = False

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "workspace_dir",
        "data_dir",
        "exports_dir",
        "default_registry_path",
    )
    @classmethod
    def _paths_should_be_relative(cls, value: Path) -> Path:
        if value.is_absolute():
            msg = f"config paths must be relative and portable: {value}"
            raise ValueError(msg)
        return value

    @property
    def database_path(self) -> Path:
        """Return the planned SQLite path under the local workspace data dir."""
        return self.data_dir / "res2jobworks.sqlite3"


def load_config(path: Path | None = None) -> Res2JobWorksConfig:
    """Load YAML config from `path`, or return validated portable defaults."""
    if path is None:
        return Res2JobWorksConfig()

    if not path.exists():
        msg = f"config file does not exist: {path}"
        raise FileNotFoundError(msg)

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        msg = "config file must contain a mapping"
        raise ValueError(msg)
    return Res2JobWorksConfig.model_validate(_normalize_paths(raw))


def _normalize_paths(raw: dict[str, Any]) -> dict[str, Any]:
    path_fields = {
        "workspace_dir",
        "data_dir",
        "exports_dir",
        "default_registry_path",
    }
    normalized = dict(raw)
    for key in path_fields & normalized.keys():
        normalized[key] = Path(normalized[key])
    return normalized
