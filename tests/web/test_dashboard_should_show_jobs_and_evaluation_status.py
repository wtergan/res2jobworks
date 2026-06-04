from apps.web.res2jobworks_web import render_dashboard_html
from tests.workflows.helpers import import_public_fixture_pair

from res2jobworks_core.commands import add_application, evaluate_job


def test_dashboard_should_show_jobs_and_evaluation_status(tmp_path) -> None:
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

    html = render_dashboard_html(database_path)

    assert '<main id="main"' in html
    assert "<table>" in html
    assert "Product Operations Analyst" in html
    assert "interested" in html
    assert "Score" in html
    assert "Deterministic rubric" in html
    assert "resume_source" in html
    assert "job_source" in html
