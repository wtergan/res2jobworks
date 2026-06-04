from pathlib import Path

import pytest

import res2jobworks_core.registry as registry_module


def test_current_directory_registry_should_not_be_implicit_fallback(
    tmp_path: Path,
    monkeypatch,
) -> None:
    unsafe_commands = tmp_path / "commands"
    unsafe_commands.mkdir()
    (unsafe_commands / "registry.yaml").write_text(
        """
version: 1
owner: unsafe
description: Unsafe current working directory registry.
commands:
  - id: unsafe.command
    description: Should not be loaded implicitly.
    phase: test
    status: planned
    inputs: []
    outputs: []
    clients: [cli]
""",
        encoding="utf-8",
    )
    installed_package = tmp_path / "site-packages" / "res2jobworks_core"
    installed_package.mkdir(parents=True)
    fake_module = installed_package / "registry.py"
    fake_module.write_text("# installed module placeholder\n", encoding="utf-8")
    monkeypatch.setattr(registry_module, "__file__", str(fake_module))
    monkeypatch.setattr(
        registry_module.resources,
        "files",
        lambda package: installed_package,
    )
    monkeypatch.chdir(tmp_path)

    with pytest.raises(FileNotFoundError, match="commands/registry.yaml"):
        registry_module.load_command_registry()

