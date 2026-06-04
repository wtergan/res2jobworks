from res2jobworks_core.commands import evaluate_job
from res2jobworks_core.repositories.sqlite import SQLiteRepository
from tests.workflows.helpers import import_public_fixture_pair


def test_job_evaluation_should_store_rubric_citations(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"
    profile, job = import_public_fixture_pair(database_path)

    envelope = evaluate_job(
        database_path,
        profile_id=profile["id"],
        job_id=job["id"],
    )

    assert envelope.ok
    evaluation = envelope.data["evaluation"]
    assert evaluation["rubric_version"] == "mvp1-deterministic-v1"
    assert evaluation["provider_kind"] == "deterministic"
    assert evaluation["score"] > 0
    assert evaluation["provider_metadata"]["dimensions"]["matched_skills"]
    assert {citation["source_table"] for citation in evaluation["citations"]} == {
        "resume_sources",
        "job_sources",
    }
    assert all(citation["quote"] for citation in evaluation["citations"])
    reloaded = SQLiteRepository(database_path).get_evaluation(evaluation["id"])
    assert reloaded["citations"] == evaluation["citations"]
