from res2jobworks_core.repositories.sqlite import REDACTED, SQLiteRepository


def test_agent_run_with_secret_fields_should_redact_values(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    agent_run = repository.record_agent_run(
        run_id="agent-run-1",
        command_id="jobs.evaluate",
        status="completed",
        input={
            "api_key": "live-key",
            "nested": {"access_token": "live-token"},
            "items": [{"password": "live-password"}],
        },
        output={"token": "output-token", "ok": True},
    )

    assert agent_run["input"]["api_key"] == REDACTED
    assert agent_run["input"]["nested"]["access_token"] == REDACTED
    assert agent_run["input"]["items"][0]["password"] == REDACTED
    assert agent_run["output"]["token"] == REDACTED
    assert agent_run["output"]["ok"] is True
