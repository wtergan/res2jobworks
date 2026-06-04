from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_agent_run_token_usage_should_not_redact_usage_counts(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    agent_run = repository.record_agent_run(
        run_id="agent-run-1",
        command_id="jobs.evaluate",
        status="completed",
        output={
            "prompt_tokens": 120,
            "total_tokens": 180,
            "token_usage": {"completion": 60},
        },
    )

    assert agent_run["output"]["prompt_tokens"] == 120
    assert agent_run["output"]["total_tokens"] == 180
    assert agent_run["output"]["token_usage"] == {"completion": 60}
