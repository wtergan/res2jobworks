import json

from apps.cli.res2jobworks_cli import main
from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job


def test_document_commands_should_run_through_cli_registry(tmp_path, capsys) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])

    exit_code = main(
        [
            "run",
            "documents.draft_cover_letter",
            "--json",
            "--input",
            f"database_path={database_path}",
            "--input",
            f"profile_id={profile['id']}",
            "--input",
            f"job_id={job['id']}",
            "--input",
            "requested_focus=Kubernetes",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["command"] == "documents.draft_cover_letter"
    assert output["data"]["draft"]["unsupported_inferences"] == ["Kubernetes"]


def test_application_answer_command_should_run_through_cli_registry(
    tmp_path,
    capsys,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])

    exit_code = main(
        [
            "run",
            "documents.draft_application_answer",
            "--json",
            "--input",
            f"database_path={database_path}",
            "--input",
            f"profile_id={profile['id']}",
            "--input",
            f"job_id={job['id']}",
            "--input",
            "question=Describe your Kubernetes production experience.",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["command"] == "documents.draft_application_answer"
    assert output["data"]["draft"]["kind"] == "application_answer"
    assert "Kubernetes" in output["data"]["draft"]["unsupported_inferences"]
