from pathlib import Path

import res2jobworks_core.seed as seed_module


def test_source_fixture_seed_should_not_depend_on_cwd(
    tmp_path: Path,
    monkeypatch,
) -> None:
    empty_package_root = tmp_path / "site-packages" / "res2jobworks_core"
    empty_package_root.mkdir(parents=True)
    original_files = seed_module.resources.files
    monkeypatch.setattr(
        seed_module.resources,
        "files",
        lambda package: (
            empty_package_root
            if package == "res2jobworks_core"
            else original_files(package)
        ),
    )
    monkeypatch.chdir(tmp_path)

    seeded = seed_module.seed_public_sample_workspace(tmp_path / "workspace.sqlite3")

    assert seeded["profile"]["id"] == "fixture-profile-jordan-avery"
    assert seeded["job"]["id"] == "fixture-job-product-operations-analyst"
