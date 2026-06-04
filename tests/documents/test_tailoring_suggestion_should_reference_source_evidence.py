from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_documents import build_tailoring_suggestions


def test_tailoring_suggestion_should_reference_source_evidence(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])

    suggestions = build_tailoring_suggestions(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    assert suggestions[0]["section"] == "summary"
    assert suggestions[0]["review_state"] == "human_review_required"
    assert {link["source_table"] for link in suggestions[0]["evidence"]} == {
        "resume_sources",
        "job_sources",
    }
    assert suggestions[0]["unsupported_inferences"] == []
