from res2jobworks_core.registry import load_command_registry


def test_available_sqlite_commands_should_accept_database_path() -> None:
    registry = load_command_registry()
    sqlite_command_ids = {
        "profile.import",
        "jobs.import",
        "jobs.evaluate",
        "applications.add",
        "applications.update",
        "applications.list",
        "applications.export",
    }

    for command_id in sqlite_command_ids:
        command = registry.by_id(command_id)
        assert command.status == "available"
        assert "database_path" in command.inputs
