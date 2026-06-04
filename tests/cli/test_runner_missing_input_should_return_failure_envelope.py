import json

from apps.cli.res2jobworks_cli import main


def test_runner_missing_input_should_return_failure_envelope(capsys) -> None:
    exit_code = main(["run", "jobs.evaluate", "--json"])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert output["ok"] is False
    assert output["command"] == "jobs.evaluate"
    assert output["errors"][0]["code"] == "validation_error"
    assert "missing required --input database_path=<value>" in output["errors"][0][
        "message"
    ]
