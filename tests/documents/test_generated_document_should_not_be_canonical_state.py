from pathlib import Path

from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_core.repositories.sqlite import SQLiteRepository
from res2jobworks_documents import build_cover_letter_draft, render_document_artifact


def test_generated_document_should_not_be_canonical_state(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    export_record = render_document_artifact(
        database_path,
        draft=draft,
        output_path=Path("exports/cover-letter.md"),
        format="markdown",
        target_table="jobs",
        target_id=job["id"],
    )

    repository = SQLiteRepository(database_path)
    assert Path("exports/cover-letter.md").exists()
    assert export_record["target_table"] == "jobs"
    assert export_record["target_id"] == job["id"]
    assert export_record["metadata"]["document_kind"] == "cover_letter"
    assert repository.get_job(job["id"]) == job
    assert repository.get_profile(profile["id"]) == profile
