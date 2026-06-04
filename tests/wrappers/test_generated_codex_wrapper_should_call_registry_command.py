from res2jobworks_core.registry import load_command_registry
from res2jobworks_skills.generator import generate_agent_wrappers


def test_generated_codex_wrapper_should_call_registry_command(tmp_path) -> None:
    output_path = tmp_path / "wrappers"

    generate_agent_wrappers(output_path=output_path, target_agents=["codex"])

    wrapper_text = (output_path / "codex" / "SKILL.md").read_text(
        encoding="utf-8",
    )
    agent_commands = [
        command
        for command in load_command_registry().commands
        if "agent" in command.clients
    ]

    assert "res2jobworks run jobs.evaluate --json" in wrapper_text
    assert "job_id=<value>" in wrapper_text
    assert "rubric_id=<value>" in wrapper_text
    assert "Status: available" in wrapper_text
    assert "Status: planned" in wrapper_text
    assert all(command.id in wrapper_text for command in agent_commands)
    assert "res2jobworks_core.commands" not in wrapper_text
    assert "SQLiteRepository" not in wrapper_text
