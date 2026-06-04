"""Command registry metadata loader and validator.

The registry is the source for future CLI, TUI, web, automation, and generated
agent-wrapper command surfaces. It describes command availability without
implementing workflow behavior during bootstrap.
"""

from importlib import resources
from pathlib import Path
from typing import Self

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

VALID_CLIENTS = {"cli", "tui", "web", "automation", "agent"}
VALID_STATUSES = {"planned", "available", "deprecated"}


class CommandMetadata(BaseModel):
    """Metadata for one planned or available product command."""

    id: str
    description: str
    phase: str
    status: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    clients: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @field_validator("id")
    @classmethod
    def _id_should_be_namespace_dot_name(cls, value: str) -> str:
        if "." not in value or value.startswith(".") or value.endswith("."):
            msg = f"command id must use a namespace.name shape: {value}"
            raise ValueError(msg)
        return value

    @field_validator("status")
    @classmethod
    def _status_should_be_known(cls, value: str) -> str:
        if value not in VALID_STATUSES:
            msg = f"unknown command status: {value}"
            raise ValueError(msg)
        return value

    @field_validator("clients")
    @classmethod
    def _clients_should_be_known(cls, value: list[str]) -> list[str]:
        unknown = sorted(set(value) - VALID_CLIENTS)
        if unknown:
            msg = f"unknown command clients: {', '.join(unknown)}"
            raise ValueError(msg)
        return value


class CommandRegistry(BaseModel):
    """Validated registry document for command metadata."""

    version: int
    owner: str
    description: str
    commands: list[CommandMetadata]

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def _command_ids_should_be_unique(self) -> Self:
        ids = [command.id for command in self.commands]
        duplicates = sorted(
            {command_id for command_id in ids if ids.count(command_id) > 1}
        )
        if duplicates:
            msg = f"duplicate command ids: {', '.join(duplicates)}"
            raise ValueError(msg)
        return self

    def by_id(self, command_id: str) -> CommandMetadata:
        """Return metadata for `command_id` or raise a clear lookup error."""
        for command in self.commands:
            if command.id == command_id:
                return command
        msg = f"unknown command id: {command_id}"
        raise KeyError(msg)


def load_command_registry(path: Path | None = None) -> CommandRegistry:
    """Load and validate the shared command registry YAML document."""
    if path is not None:
        registry_text = path.read_text(encoding="utf-8")
    else:
        registry_text = default_registry_text()
    raw = yaml.safe_load(registry_text)
    if not isinstance(raw, dict):
        msg = "registry must be a mapping"
        raise ValueError(msg)
    return CommandRegistry.model_validate(raw)


def default_registry_text() -> str:
    """Read packaged registry data, falling back to the source-tree registry."""
    packaged = resources.files("res2jobworks_core").joinpath("registry.yaml")
    if packaged.is_file():
        return packaged.read_text(encoding="utf-8")

    return default_registry_path().read_text(encoding="utf-8")


def default_registry_path() -> Path:
    """Find the source-tree `commands/registry.yaml` for local development."""
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "commands" / "registry.yaml"
        if candidate.exists() and (parent / "pyproject.toml").exists():
            return candidate
    msg = "could not locate commands/registry.yaml"
    raise FileNotFoundError(msg)
