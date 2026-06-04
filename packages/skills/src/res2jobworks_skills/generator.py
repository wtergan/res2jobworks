"""Generate agent wrappers from the shared command registry.

This module owns only wrapper artifact rendering. Product behavior stays in the
core command handlers and future CLI/API runners; generated wrappers point
agents at those contracts instead of importing core workflow modules or
duplicating scoring, persistence, or export logic.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from res2jobworks_core.registry import (
    CommandMetadata,
    CommandRegistry,
    load_command_registry,
)

FIRST_CLASS_AGENTS = ("codex", "hermes")
STUB_AGENTS = ("claude", "opencode", "gemini")
SUPPORTED_AGENTS = FIRST_CLASS_AGENTS + STUB_AGENTS
DEFAULT_COMMAND_RUNNER = "res2jobworks run"


@dataclass(frozen=True)
class GeneratedWrapperFile:
    """One wrapper artifact produced by the registry-driven generator."""

    agent: str
    path: Path


def generate_agent_wrappers(
    *,
    output_path: Path | str,
    registry_path: Path | str | None = None,
    target_agents: Sequence[str] | None = None,
    command_runner: str = DEFAULT_COMMAND_RUNNER,
) -> list[GeneratedWrapperFile]:
    """Generate agent wrapper artifacts from registry metadata.

    The generated wrappers are thin instructions around the shared CLI/API
    command contract. They never call workflow internals or embed product rules.
    """
    registry = load_command_registry(
        Path(registry_path) if registry_path is not None else None,
    )
    output_root = Path(output_path)
    output_root.mkdir(parents=True, exist_ok=True)
    agents = _resolve_agents(target_agents)
    commands = _agent_commands(registry)

    generated: list[GeneratedWrapperFile] = []
    for agent in agents:
        relative_path, content = _render_agent_wrapper(
            agent,
            registry=registry,
            commands=commands,
            command_runner=command_runner,
        )
        wrapper_path = output_root / relative_path
        wrapper_path.parent.mkdir(parents=True, exist_ok=True)
        wrapper_path.write_text(content, encoding="utf-8")
        generated.append(GeneratedWrapperFile(agent=agent, path=wrapper_path))

    manifest_path = output_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "registry_version": registry.version,
                "registry_owner": registry.owner,
                "command_runner": command_runner,
                "agents": agents,
                "command_ids": [command.id for command in commands],
                "generated_files": [
                    str(file.path.relative_to(output_root)) for file in generated
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    generated.append(GeneratedWrapperFile(agent="manifest", path=manifest_path))
    return generated


def main(argv: Sequence[str] | None = None) -> int:
    """Run wrapper generation from a source checkout or installed environment."""
    parser = argparse.ArgumentParser(
        description="Generate res2jobWorks agent wrappers from commands/registry.yaml.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Directory where wrapper artifacts should be written.",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        help="Optional command registry YAML path. Defaults to the packaged registry.",
    )
    parser.add_argument(
        "--target-agent",
        action="append",
        choices=(*SUPPORTED_AGENTS, "all"),
        help="Agent wrapper to generate. Repeat for multiple agents; default is all.",
    )
    parser.add_argument(
        "--command-runner",
        default=DEFAULT_COMMAND_RUNNER,
        help="Shared CLI/API runner command used in generated wrapper instructions.",
    )
    args = parser.parse_args(argv)

    generated = generate_agent_wrappers(
        output_path=args.output,
        registry_path=args.registry,
        target_agents=args.target_agent,
        command_runner=args.command_runner,
    )
    print(
        json.dumps(
            {"generated_files": [str(file.path) for file in generated]},
            indent=2,
            sort_keys=True,
        ),
    )
    return 0


def _resolve_agents(target_agents: Sequence[str] | None) -> list[str]:
    if not target_agents or "all" in target_agents:
        return list(SUPPORTED_AGENTS)

    unknown = sorted(set(target_agents) - set(SUPPORTED_AGENTS))
    if unknown:
        msg = f"unknown target agents: {', '.join(unknown)}"
        raise ValueError(msg)

    return list(dict.fromkeys(target_agents))


def _agent_commands(registry: CommandRegistry) -> list[CommandMetadata]:
    return [command for command in registry.commands if "agent" in command.clients]


def _render_agent_wrapper(
    agent: str,
    *,
    registry: CommandRegistry,
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> tuple[Path, str]:
    if agent == "codex":
        return Path("codex/SKILL.md"), _render_codex_wrapper(
            registry,
            commands,
            command_runner,
        )
    if agent == "hermes":
        return Path("hermes/res2jobworks.md"), _render_hermes_wrapper(
            registry,
            commands,
            command_runner,
        )
    return Path(f"{agent}/README.md"), _render_stub_wrapper(
        agent,
        registry,
        commands,
        command_runner,
    )


def _render_codex_wrapper(
    registry: CommandRegistry,
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> str:
    return "\n".join(
        [
            "---",
            "name: res2jobworks",
            "description: Generated wrapper for res2jobWorks command contracts.",
            "---",
            "",
            "# res2jobWorks Codex Wrapper",
            "",
            _registry_notice(registry),
            "",
            "## Contract",
            "",
            f"- Call `{command_runner} <command-id> --json` for product behavior.",
            "- Return the JSON command envelope exactly as emitted by the runner.",
            (
                "- Do not import core modules, write SQLite directly, "
                "or reimplement scoring."
            ),
            (
                "- Treat planned commands as documented future contracts, "
                "not callable work."
            ),
            "",
            _render_command_catalog(commands, command_runner),
        ],
    ).rstrip() + "\n"


def _render_hermes_wrapper(
    registry: CommandRegistry,
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> str:
    return "\n".join(
        [
            "# Hermes res2jobWorks Wrapper",
            "",
            _registry_notice(registry),
            "",
            "## Runtime Contract",
            "",
            f"- Use `{command_runner} <command-id> --json` for every command call.",
            "- Return the JSON command envelope to the user or calling workflow.",
            "- Do not implement product logic inside Hermes.",
            "- Keep user data local and do not submit job applications by default.",
            "",
            _render_command_catalog(commands, command_runner),
        ],
    ).rstrip() + "\n"


def _render_stub_wrapper(
    agent: str,
    registry: CommandRegistry,
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> str:
    return "\n".join(
        [
            f"# {agent} wrapper stub",
            "",
            _registry_notice(registry),
            "",
            (
                "This format is intentionally documented as a stub because the "
                f"{agent} wrapper format is not stable in this plan slice."
            ),
            "",
            "## Required Contract",
            "",
            f"- Call `{command_runner} <command-id> --json` for product behavior.",
            "- Return the JSON command envelope without reshaping it.",
            "- Do not embed res2jobWorks product logic in the agent wrapper.",
            "",
            _render_command_catalog(commands, command_runner),
        ],
    ).rstrip() + "\n"


def _render_command_catalog(
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> str:
    available = [command for command in commands if command.status == "available"]
    planned = [command for command in commands if command.status != "available"]
    sections = [
        "## Available Commands",
        "",
        _render_commands(available, command_runner),
    ]

    if planned:
        sections.extend(
            [
                "",
                "## Planned Commands",
                "",
                (
                    "These commands are generated from the registry for parity, "
                    "but should not be called until their status becomes available."
                ),
                "",
                _render_commands(planned, command_runner),
            ],
        )
    return "\n".join(sections).rstrip()


def _render_commands(
    commands: Sequence[CommandMetadata],
    command_runner: str,
) -> str:
    blocks: list[str] = []
    for command in commands:
        blocks.extend(
            [
                f"### {command.id}",
                "",
                command.description,
                "",
                f"- Status: {command.status}",
                f"- Phase: {command.phase}",
                f"- Inputs: {_format_names(command.inputs)}",
                f"- Outputs: {_format_names(command.outputs)}",
                "",
                "Invocation:",
                "",
                "```bash",
                _invocation_for(command, command_runner),
                "```",
                "",
            ],
        )
    return "\n".join(blocks).rstrip()


def _invocation_for(command: CommandMetadata, command_runner: str) -> str:
    parts = [command_runner, command.id, "--json"]
    for input_name in command.inputs:
        parts.extend(["--input", f"{input_name}=<value>"])
    return " ".join(parts)


def _format_names(names: Sequence[str]) -> str:
    if not names:
        return "none"
    return ", ".join(names)


def _registry_notice(registry: CommandRegistry) -> str:
    return (
        f"Generated from command registry version {registry.version} "
        f"owned by `{registry.owner}`."
    )
