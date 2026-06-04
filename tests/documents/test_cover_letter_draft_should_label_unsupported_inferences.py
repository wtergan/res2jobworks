import json

from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import evaluate_job
from res2jobworks_core.db.connection import connect
from res2jobworks_documents import build_cover_letter_draft


def test_cover_letter_draft_should_label_unsupported_inferences(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluate_job(database_path, profile_id=profile["id"], job_id=job["id"])

    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
        requested_focus=("Kubernetes",),
    )

    assert draft.review_state == "human_review_required"
    assert draft.unsupported_inferences == ("Kubernetes",)
    assert "Unsupported inference labels: Kubernetes" in draft.body
    assert draft.evidence


def test_provider_metadata_skill_should_not_become_claim_without_evidence(
    tmp_path,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluation = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    ).data["evaluation"]
    with connect(database_path) as connection, connection:
        connection.execute(
            """
            UPDATE evaluations
            SET provider_metadata_json = ?
            WHERE id = ?
            """,
            (
                json.dumps({"dimensions": {"matched_skills": ["Kubernetes"]}}),
                evaluation["id"],
            ),
        )

    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
        evaluation_id=evaluation["id"],
    )

    assert "supports emphasis on Kubernetes" not in draft.body
    assert draft.unsupported_inferences == ("Kubernetes",)


def test_provider_metadata_skill_should_require_term_boundary_evidence(
    tmp_path,
) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)
    evaluation = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    ).data["evaluation"]
    with connect(database_path) as connection, connection:
        connection.execute(
            """
            UPDATE evaluations
            SET provider_metadata_json = ?
            WHERE id = ?
            """,
            (
                json.dumps({"dimensions": {"matched_skills": ["R"]}}),
                evaluation["id"],
            ),
        )

    draft = build_cover_letter_draft(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
        evaluation_id=evaluation["id"],
    )

    assert "supports emphasis on R." not in draft.body
    assert draft.unsupported_inferences == ("R",)
