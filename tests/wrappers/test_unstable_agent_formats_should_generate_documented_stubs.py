from res2jobworks_skills.generator import generate_agent_wrappers


def test_unstable_agent_formats_should_generate_documented_stubs(tmp_path) -> None:
    output_path = tmp_path / "wrappers"

    generate_agent_wrappers(
        output_path=output_path,
        target_agents=["claude", "opencode", "gemini"],
    )

    for agent in ["claude", "opencode", "gemini"]:
        stub_text = (output_path / agent / "README.md").read_text(encoding="utf-8")
        assert f"{agent} wrapper stub" in stub_text
        assert "format is intentionally documented as a stub" in stub_text
        assert "res2jobworks run workspace.init --json" in stub_text
        assert "Generated from command registry version 1" in stub_text
