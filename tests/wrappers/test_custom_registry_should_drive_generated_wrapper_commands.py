from pathlib import Path

from res2jobworks_skills.generator import generate_agent_wrappers


def test_custom_registry_should_drive_generated_wrapper_commands(tmp_path) -> None:
    registry_path = tmp_path / "registry.yaml"
    registry_path.write_text(
        """
version: 1
owner: test
description: Custom registry for generator behavior.
commands:
  - id: custom.echo
    description: Echo custom input through the shared contract.
    phase: test
    status: available
    inputs:
      - message
    outputs:
      - echoed_message
    clients:
      - agent
""".lstrip(),
        encoding="utf-8",
    )
    output_path = tmp_path / "wrappers"

    generate_agent_wrappers(
        registry_path=Path(registry_path),
        output_path=output_path,
        target_agents=["codex"],
    )

    wrapper_text = (output_path / "codex" / "SKILL.md").read_text(
        encoding="utf-8",
    )

    assert "custom.echo" in wrapper_text
    assert "message=<value>" in wrapper_text
    assert "echoed_message" in wrapper_text
    assert "jobs.evaluate" not in wrapper_text
