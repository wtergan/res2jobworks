import json

from apps.cli.res2jobworks_cli import main


def test_automation_capture_runner_should_return_command_envelope(
    tmp_path,
    capsys,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"

    exit_code = main(
        [
            "run",
            "automation.capture_job",
            "--json",
            "--input",
            f"database_path={database_path}",
            "--input",
            "source_url=https://example.test/jobs/runner",
            "--input",
            "source_text=# Runner Analyst\n\n## Organization\nExample Labs\n",
            "--input",
            "captured_at=2026-06-04T12:00:00Z",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["command"] == "automation.capture_job"
    assert output["data"]["job"]["title"] == "Runner Analyst"
    assert output["data"]["job_source"]["source_url"] == (
        "https://example.test/jobs/runner"
    )
