from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_agent_run_should_persist_without_secret_fields(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    agent_run = repository.record_agent_run(
        run_id="agent-run-1",
        command_id="jobs.evaluate",
        status="completed",
        input={"job_id": "job-1"},
        output={"ok": True},
    )

    assert agent_run["provider"] == "local"
    assert agent_run["input"] == {"job_id": "job-1"}
    assert agent_run["output"] == {"ok": True}
