from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_documents import build_resume_diff, build_tailoring_suggestions


def test_resume_diff_should_preserve_original_sections(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    suggestion = build_tailoring_suggestions(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )[0]

    diff = build_resume_diff(suggestion)

    assert diff["section"] == "summary"
    assert diff["original"] == suggestion["original"]
    assert diff["proposed"] != diff["original"]
    assert diff["reversible"] is True
    assert diff["review_state"] == "human_review_required"
