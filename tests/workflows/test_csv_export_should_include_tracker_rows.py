from pathlib import Path

from res2jobworks_core.commands import add_application, export_applications
from tests.workflows.helpers import import_public_fixture_pair


def test_csv_export_should_include_tracker_rows(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    database_path = tmp_path / "workspace.sqlite3"
    _, job = import_public_fixture_pair(database_path)
    add_application(database_path, job_id=job["id"], status="interested")

    envelope = export_applications(
        database_path,
        output_path=Path("exports/tracker.csv"),
        format="csv",
    )

    assert envelope.ok
    csv_text = Path(envelope.files[0]).read_text(encoding="utf-8")
    assert csv_text.splitlines()[0] == (
        "application_id,job_id,employer,title,status,evaluation_score"
    )
    assert "Product Operations Analyst" in csv_text
    assert "interested" in csv_text
