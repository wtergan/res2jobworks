from pathlib import Path

from res2jobworks_core.commands import import_profile


def test_duplicate_profile_import_should_return_failure_envelope(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    source_path = Path("templates/profile-example.yaml")

    first = import_profile(
        database_path,
        source_path=source_path,
        source_type="yaml_fixture",
    )
    second = import_profile(
        database_path,
        source_path=source_path,
        source_type="yaml_fixture",
    )

    assert first.ok
    assert not second.ok
    assert second.command == "profile.import"
    assert second.errors[0].code in {"IntegrityError", "OperationalError"}
