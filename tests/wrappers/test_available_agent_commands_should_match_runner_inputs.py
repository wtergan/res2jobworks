from apps.cli.res2jobworks_cli import _RUNNERS

from res2jobworks_core.registry import load_command_registry
from res2jobworks_skills.generator import generate_agent_wrappers


def test_available_agent_commands_should_match_runner_inputs(tmp_path) -> None:
    output_path = tmp_path / "wrappers"
    registry = load_command_registry()

    generate_agent_wrappers(output_path=output_path, target_agents=["codex"])

    wrapper_text = (output_path / "codex" / "SKILL.md").read_text(
        encoding="utf-8",
    )
    for command in registry.commands:
        if command.status != "available" or "agent" not in command.clients:
            continue
        assert command.id in _RUNNERS
        invocation = f"res2jobworks run {command.id} --json"
        for input_name in command.inputs:
            invocation += f" --input {input_name}=<value>"
        assert invocation in wrapper_text
