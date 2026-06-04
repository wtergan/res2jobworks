from pathlib import Path

from res2jobworks_core.commands import add_application, export_applications
from tests.workflows.helpers import import_public_fixture_pair


def test_duplicate_export_should_return_failure_envelope(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    database_path = tmp_path / "workspace.sqlite3"
    _, job = import_public_fixture_pair(database_path)
    add_application(database_path, job_id=job["id"])

    first = export_applications(
        database_path,
        output_path=Path("exports/tracker.csv"),
        format="csv",
    )
    second = export_applications(
        database_path,
        output_path=Path("exports/tracker.csv"),
        format="csv",
    )

    assert first.ok
    assert not second.ok
    assert second.command == "applications.export"
    assert second.errors[0].code == "IntegrityError"
