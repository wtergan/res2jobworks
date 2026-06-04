"""Stable command-envelope contracts shared by every client surface.

All interfaces return the same shape so CLI, TUI, web, automation, and agent
wrappers can interoperate without duplicating product logic.
"""

from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CommandError(BaseModel):
    """Structured command failure detail safe for clients and agent wrappers."""

    code: str
    message: str
    field: str | None = None

    model_config = ConfigDict(extra="forbid")


class CommandEnvelope(BaseModel):
    """Stable command result envelope for res2jobWorks commands."""

    ok: bool
    command: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    data: dict[str, Any] = Field(default_factory=dict)
    files: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[CommandError] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def _failure_should_report_errors(self) -> Self:
        if not self.ok and not self.errors:
            msg = "failed command envelopes must include at least one error"
            raise ValueError(msg)
        if self.ok and self.errors:
            msg = "successful command envelopes cannot include errors"
            raise ValueError(msg)
        return self

    @classmethod
    def success(
        cls,
        command: str,
        *,
        inputs: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[str] | None = None,
        warnings: list[str] | None = None,
    ) -> Self:
        """Build a successful command envelope with explicit output fields."""
        return cls(
            ok=True,
            command=command,
            inputs=inputs or {},
            data=data or {},
            files=files or [],
            warnings=warnings or [],
            errors=[],
        )

    @classmethod
    def failure(
        cls,
        command: str,
        *,
        errors: list[CommandError],
        inputs: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: list[str] | None = None,
        warnings: list[str] | None = None,
    ) -> Self:
        """Build a failed command envelope that cannot hide error details."""
        return cls(
            ok=False,
            command=command,
            inputs=inputs or {},
            data=data or {},
            files=files or [],
            warnings=warnings or [],
            errors=errors,
        )

