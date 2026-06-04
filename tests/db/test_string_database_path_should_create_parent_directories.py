from res2jobworks_core.db.migrations import apply_migrations


def test_string_database_path_should_create_parent_directories(tmp_path) -> None:
    database_path = tmp_path / "nested" / "workspace.sqlite3"

    version = apply_migrations(str(database_path))

    assert version == 1
    assert database_path.exists()
