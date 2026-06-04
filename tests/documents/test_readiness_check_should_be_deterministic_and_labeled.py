from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_documents import (
    analyze_document_readiness,
    build_cover_letter_draft,
)


def test_readiness_check_should_be_deterministic_and_labeled(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])
    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    report = analyze_document_readiness(
        draft,
        target_keywords=("product operations", "markdown", "sql"),
    )

    assert {check["name"] for check in report["checks"]} == {
        "readability.average_sentence_length",
        "ats.keyword_coverage",
    }
    assert all(check["method"] == "deterministic" for check in report["checks"])
    assert all(
        check["label"] == "local deterministic check" for check in report["checks"]
    )
