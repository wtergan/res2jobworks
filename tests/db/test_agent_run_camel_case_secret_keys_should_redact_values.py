from res2jobworks_core.repositories.sqlite import REDACTED, SQLiteRepository


def test_agent_run_camel_case_secret_keys_should_redact_values(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    agent_run = repository.record_agent_run(
        run_id="agent-run-1",
        command_id="jobs.evaluate",
        status="completed",
        input={
            "accessToken": "live-token",
            "refreshToken": "live-refresh-token",
            "clientSecret": "live-client-secret",
            "tokenUsage": {"totalTokens": 10},
        },
    )

    assert agent_run["input"]["accessToken"] == REDACTED
    assert agent_run["input"]["refreshToken"] == REDACTED
    assert agent_run["input"]["clientSecret"] == REDACTED
    assert agent_run["input"]["tokenUsage"]["totalTokens"] == 10
