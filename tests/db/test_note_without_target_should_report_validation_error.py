import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_note_without_target_should_report_validation_error(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    with pytest.raises(RepositoryError, match="note must reference"):
        repository.add_note(note_id="note-1", body="Fictional note")
