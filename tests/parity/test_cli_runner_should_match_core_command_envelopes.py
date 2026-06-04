import json

from apps.cli.res2jobworks_cli import main

from res2jobworks_core.commands import evaluate_job, import_job, import_profile


def test_cli_runner_should_match_core_command_envelopes(tmp_path, capsys) -> None:
    direct_database_path = tmp_path / "direct.sqlite3"
    cli_database_path = tmp_path / "cli.sqlite3"
    profile_source = "name: Jordan Avery\nheadline: Operations analyst\n"
    job_source = "# Product Operations Analyst\n\n## Organization\nExample Labs\n"

    direct_profile = import_profile(
        direct_database_path,
        source_text=profile_source,
        source_type="yaml",
    ).data["profile"]
    direct_job = import_job(
        direct_database_path,
        source_text=job_source,
        source_type="markdown",
    ).data["job"]
    direct = evaluate_job(
        direct_database_path,
        profile_id=direct_profile["id"],
        job_id=direct_job["id"],
    ).model_dump(mode="json")

    assert main(
        [
            "run",
            "profile.import",
            "--json",
            "--input",
            f"database_path={cli_database_path}",
            "--input",
            f"source_text={profile_source}",
            "--input",
            "source_type=yaml",
        ]
    ) == 0
    cli_profile = json.loads(capsys.readouterr().out)["data"]["profile"]

    assert main(
        [
            "run",
            "jobs.import",
            "--json",
            "--input",
            f"database_path={cli_database_path}",
            "--input",
            f"source_text={job_source}",
            "--input",
            "source_type=markdown",
        ]
    ) == 0
    cli_job = json.loads(capsys.readouterr().out)["data"]["job"]

    assert main(
        [
            "run",
            "jobs.evaluate",
            "--json",
            "--input",
            f"database_path={cli_database_path}",
            "--input",
            f"profile_id={cli_profile['id']}",
            "--input",
            f"job_id={cli_job['id']}",
        ]
    ) == 0
    cli = json.loads(capsys.readouterr().out)

    assert cli["ok"] is True
    assert cli["command"] == direct["command"]
    assert cli["data"]["evaluation"]["score"] == direct["data"]["evaluation"]["score"]
    assert len(cli["data"]["citations"]) == len(direct["data"]["citations"])
