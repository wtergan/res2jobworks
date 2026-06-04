import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_agent_run_status_should_be_known_value(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    with pytest.raises(RepositoryError, match="status must be one of"):
        repository.record_agent_run(
            run_id="agent-run-1",
            command_id="evaluate-job-fit",
            status="mystery",
        )
