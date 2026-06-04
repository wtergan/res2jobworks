from pathlib import Path


def test_local_workspace_directory_should_be_gitignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")

    assert ".res2jobworks/" in gitignore

