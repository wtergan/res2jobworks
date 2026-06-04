import pytest

from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository


def test_exports_should_reference_canonical_records(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )
    application = repository.create_application(
        application_id="application-1",
        job_id="job-1",
        status="interested",
        event_id="event-1",
    )

    export = repository.record_export(
        export_id="export-1",
        export_type="tracker",
        format="csv",
        target_table="applications",
        target_id=application["id"],
        path="exports/tracker.csv",
    )

    assert export["target_table"] == "applications"
    assert export["target_id"] == "application-1"
    with pytest.raises(RepositoryError, match="does not exist"):
        repository.record_export(
            export_id="export-2",
            export_type="tracker",
            format="csv",
            target_table="applications",
            target_id="missing",
            path="exports/missing.csv",
        )


def test_document_exports_should_allow_pdf_and_docx_formats(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")
    repository.create_job(
        job_id="job-1",
        employer="Example Cooperative",
        title="Operations Analyst",
        description="Fictional fixture job description",
    )

    pdf_export = repository.record_export(
        export_id="export-pdf",
        export_type="cover_letter_document",
        format="pdf",
        target_table="jobs",
        target_id="job-1",
        path="exports/cover-letter.pdf",
    )
    docx_export = repository.record_export(
        export_id="export-docx",
        export_type="cover_letter_document",
        format="docx",
        target_table="jobs",
        target_id="job-1",
        path="exports/cover-letter.docx",
    )

    assert pdf_export["format"] == "pdf"
    assert docx_export["format"] == "docx"
