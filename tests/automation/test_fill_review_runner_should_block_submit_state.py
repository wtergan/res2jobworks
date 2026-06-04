import json

from apps.cli.res2jobworks_cli import main


def test_fill_review_runner_should_block_submit_state(capsys) -> None:
    exit_code = main(
        [
            "run",
            "automation.prepare_fill_review",
            "--json",
            "--input",
            'fields_json={"full_name":"Jordan Avery"}',
            "--input",
            "review_state=ready_to_submit",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert output["errors"][0]["code"] == "review_required"
