from pathlib import Path

import res2jobworks_core.seed as seed_module


def test_packaged_fixture_seed_should_create_sample_workspace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    packaged_root = tmp_path / "site-packages" / "res2jobworks_core"
    packaged_fixtures = packaged_root / "fixtures"
    packaged_fixtures.mkdir(parents=True)
    (packaged_fixtures / "profile-example.yaml").write_text(
        Path("templates/profile-example.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (packaged_fixtures / "sample-job.md").write_text(
        Path("examples/jobs/sample-job.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    original_files = seed_module.resources.files
    monkeypatch.setattr(
        seed_module.resources,
        "files",
        lambda package: (
            packaged_root
            if package == "res2jobworks_core"
            else original_files(package)
        ),
    )
    monkeypatch.chdir(tmp_path)

    seeded = seed_module.seed_public_sample_workspace(tmp_path / "workspace.sqlite3")

    assert seeded["profile"]["id"] == "fixture-profile-jordan-avery"
    assert seeded["job"]["id"] == "fixture-job-product-operations-analyst"
