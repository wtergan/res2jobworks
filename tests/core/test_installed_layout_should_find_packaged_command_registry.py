from pathlib import Path

import res2jobworks_core.registry as registry_module


def test_installed_layout_should_find_packaged_command_registry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    installed_package = tmp_path / "site-packages" / "res2jobworks_core"
    installed_package.mkdir(parents=True)
    packaged_registry = installed_package / "registry.yaml"
    packaged_registry.write_text(
        Path("commands/registry.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        registry_module.resources,
        "files",
        lambda package: installed_package,
    )
    monkeypatch.chdir(tmp_path)

    loaded = registry_module.load_command_registry()

    assert loaded.by_id("jobs.evaluate").id == "jobs.evaluate"

