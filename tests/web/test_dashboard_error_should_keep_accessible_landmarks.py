from apps.web import res2jobworks_web

from res2jobworks_core.contracts import CommandEnvelope, CommandError


def test_dashboard_error_should_keep_accessible_landmarks(
    monkeypatch,
    tmp_path,
) -> None:
    def fail_dashboard_jobs(_database_path):
        return CommandEnvelope.failure(
            "jobs.list",
            errors=[
                CommandError(
                    code="repository_error",
                    message="database unavailable",
                )
            ],
        ), []

    monkeypatch.setattr(res2jobworks_web, "load_dashboard_jobs", fail_dashboard_jobs)

    html = res2jobworks_web.render_dashboard_html(tmp_path / "workspace.sqlite3")

    assert 'href="#main"' in html
    assert '<main id="main"' in html
    assert "<h1>Dashboard unavailable</h1>" in html
    assert 'role="alert"' in html
