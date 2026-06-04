from res2jobworks_core.registry import load_command_registry


def test_registry_entries_should_have_required_metadata() -> None:
    registry = load_command_registry()
    available_command_ids = {
        command.id for command in registry.commands if command.status == "available"
    }

    assert registry.version == 1
    assert registry.by_id("jobs.evaluate").outputs == ["evaluation", "citations"]
    assert registry.by_id("skills.generate").clients == ["cli", "agent"]
    assert all(command.description for command in registry.commands)
    assert all(command.phase for command in registry.commands)
    assert available_command_ids == {
        "workspace.init",
        "profile.import",
        "profile.show",
        "jobs.import",
        "jobs.evaluate",
        "jobs.list",
        "jobs.show",
        "applications.add",
        "applications.update",
        "applications.list",
        "applications.export",
        "automation.capture_job",
        "automation.prepare_fill_review",
    }
    assert all(
        command.status == "planned"
        for command in registry.commands
        if command.id not in available_command_ids
    )
