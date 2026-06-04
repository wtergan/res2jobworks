from apps.cli.res2jobworks_cli import main

from res2jobworks_core.registry import load_command_registry


def test_default_automation_should_not_submit_application(capsys) -> None:
    registry = load_command_registry()

    available_ids = {
        command.id for command in registry.commands if command.status == "available"
    }
    assert not any("submit" in command_id for command_id in available_ids)

    exit_code = main(["run", "automation.submit", "--json"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "unknown_command" in output
