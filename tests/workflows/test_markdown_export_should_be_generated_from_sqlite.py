from pathlib import Path

from res2jobworks_core.commands import (
    add_application,
    evaluate_job,
    export_applications,
)
from res2jobworks_core.repositories.sqlite import SQLiteRepository
from tests.workflows.helpers import import_public_fixture_pair


def test_markdown_export_should_be_generated_from_sqlite(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluation = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    ).data["evaluation"]
    add_application(
        database_path,
        job_id=job["id"],
        evaluation_id=evaluation["id"],
        status="interested",
    )

    envelope = export_applications(
        database_path,
        output_path=Path("exports/tracker.md"),
        format="markdown",
    )

    assert envelope.ok
    output = Path(envelope.files[0])
    assert output.read_text(encoding="utf-8").startswith(
        "# res2jobWorks Application Tracker",
    )
    assert "Product Operations Analyst" in output.read_text(encoding="utf-8")
    exports = SQLiteRepository(database_path).list_exports()
    assert exports[-1]["path"] == "exports/tracker.md"
    assert exports[-1]["metadata"]["application_count"] == 1
