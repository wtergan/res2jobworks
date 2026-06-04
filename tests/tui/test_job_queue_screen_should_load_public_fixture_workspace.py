from apps.tui.res2jobworks_tui import render_dashboard
from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import add_application, evaluate_job


def test_job_queue_screen_should_load_public_fixture_workspace(tmp_path) -> None:
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

    rendered = render_dashboard(database_path)

    assert "Product Operations Analyst" in rendered
    assert "interested" in rendered
    assert "Deterministic rubric" in rendered
