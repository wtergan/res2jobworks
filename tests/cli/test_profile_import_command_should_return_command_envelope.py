import json
from pathlib import Path

from apps.cli.res2jobworks_cli import main


def test_profile_import_command_should_return_command_envelope(
    tmp_path,
    capsys,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"

    exit_code = main(
        [
            "--json",
            "profile.import",
            "--database-path",
            str(database_path),
            "--source-path",
            "templates/profile-example.yaml",
            "--source-type",
            "yaml_fixture",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["ok"] is True
    assert output["command"] == "profile.import"
    assert output["data"]["profile"]["display_name"] == "Jordan Avery"
    assert Path(database_path).exists()
