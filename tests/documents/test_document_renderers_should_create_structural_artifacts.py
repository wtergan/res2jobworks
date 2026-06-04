import zipfile
from io import BytesIO

import pytest
from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository
from res2jobworks_documents import (
    build_cover_letter_draft,
    render_document_artifact,
    render_docx_document,
    render_pdf_document,
)


def test_document_renderers_should_create_structural_artifacts(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    docx_bytes = render_docx_document(draft)
    pdf_bytes = render_pdf_document(draft)

    with zipfile.ZipFile(BytesIO(docx_bytes)) as archive:
        assert "word/document.xml" in archive.namelist()
        assert b"Provenance" in archive.read("word/document.xml")
    assert pdf_bytes.startswith(b"%PDF-1.4")
    assert b"%%EOF" in pdf_bytes


def test_document_renderer_should_not_leave_final_artifact_when_export_record_fails(
    tmp_path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )
    monkeypatch.chdir(tmp_path)
    output_path = tmp_path / "exports" / "cover-letter.md"
    relative_output_path = "exports/cover-letter.md"

    def fail_record_export(self, **kwargs):  # noqa: ANN001, ANN202
        raise RepositoryError("record export failed")

    monkeypatch.setattr(SQLiteRepository, "record_export", fail_record_export)

    with pytest.raises(RepositoryError):
        render_document_artifact(
            database_path,
            draft=draft,
            output_path=relative_output_path,
            format="markdown",
            target_table="jobs",
            target_id=job["id"],
        )

    assert not output_path.exists()
    assert not list(output_path.parent.glob("*.tmp"))
