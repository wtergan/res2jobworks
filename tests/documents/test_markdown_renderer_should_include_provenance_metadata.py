from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_documents import build_cover_letter_draft, render_markdown_document


def test_markdown_renderer_should_include_provenance_metadata(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    markdown = render_markdown_document(draft)

    assert "## Provenance" in markdown
    assert "resume_sources:" in markdown
    assert "job_sources:" in markdown
    assert "Review state: human_review_required" in markdown
