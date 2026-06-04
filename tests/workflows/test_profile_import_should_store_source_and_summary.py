from pathlib import Path

from res2jobworks_core.commands import import_profile
from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_profile_import_should_store_source_and_summary(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    source_path = Path("templates/profile-example.yaml")

    envelope = import_profile(
        database_path,
        source_path=source_path,
        source_type="yaml_fixture",
    )

    assert envelope.ok
    profile = envelope.data["profile"]
    resume_source = envelope.data["resume_source"]
    assert profile["display_name"] == "Jordan Avery"
    assert "workflow analysis" in profile["skills"]
    assert resume_source["profile_id"] == profile["id"]
    assert resume_source["content"] == source_path.read_text(encoding="utf-8")
    assert SQLiteRepository(database_path).get_profile(profile["id"]) == profile
