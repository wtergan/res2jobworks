from res2jobworks_skills.generator import generate_agent_wrappers


def test_generated_hermes_wrapper_should_call_registry_command(tmp_path) -> None:
    output_path = tmp_path / "wrappers"

    generate_agent_wrappers(output_path=output_path, target_agents=["hermes"])

    wrapper_text = (output_path / "hermes" / "res2jobworks.md").read_text(
        encoding="utf-8",
    )

    assert "Hermes res2jobWorks Wrapper" in wrapper_text
    assert "res2jobworks run applications.export --json" in wrapper_text
    assert "--input output_path=<value>" in wrapper_text
    assert "Return the JSON command envelope" in wrapper_text
    assert "Do not implement product logic inside Hermes" in wrapper_text
