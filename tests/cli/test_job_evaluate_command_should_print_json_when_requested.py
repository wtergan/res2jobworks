import json

from apps.cli.res2jobworks_cli import main


def test_job_evaluate_command_should_print_json_when_requested(
    tmp_path,
    capsys,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    main(
        [
            "profile.import",
            "--database-path",
            str(database_path),
            "--source-path",
            "templates/profile-example.yaml",
            "--source-type",
            "yaml_fixture",
        ]
    )
    main(
        [
            "jobs.import",
            "--database-path",
            str(database_path),
            "--source-path",
            "examples/jobs/sample-job.md",
            "--source-type",
            "markdown_fixture",
        ]
    )
    capsys.readouterr()

    exit_code = main(
        [
            "--json",
            "jobs.evaluate",
            "--database-path",
            str(database_path),
            "--profile-id",
            "profile-jordan-avery",
            "--job-id",
            "job-product-operations-analyst",
            "--rubric-id",
            "mvp1-deterministic-v1",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["command"] == "jobs.evaluate"
    assert output["data"]["evaluation"]["rubric_version"] == "mvp1-deterministic-v1"
    assert len(output["data"]["citations"]) == 2
