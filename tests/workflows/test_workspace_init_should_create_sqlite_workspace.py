from pathlib import Path

from res2jobworks_core.commands import init_workspace


def test_workspace_init_should_create_sqlite_workspace(tmp_path: Path) -> None:
    envelope = init_workspace(tmp_path)

    assert envelope.ok
    metadata = envelope.data["workspace_metadata"]
    assert Path(metadata["database_path"]).exists()
    assert Path(metadata["exports_dir"]).exists()
