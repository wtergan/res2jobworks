from res2jobworks_core.db.migrations import (
    apply_migrations,
    current_version,
    table_names,
)


def test_empty_workspace_should_apply_all_migrations(tmp_path) -> None:
    database_path = tmp_path / "workspace.sqlite3"

    version = apply_migrations(database_path)
    second_version = apply_migrations(database_path)

    assert version == 2
    assert second_version == 2
    assert current_version(database_path) == 2
    assert {
        "schema_migrations",
        "profiles",
        "resume_sources",
        "jobs",
        "job_sources",
        "evaluations",
        "evaluation_citations",
        "applications",
        "application_status_events",
        "notes",
        "exports",
        "agent_runs",
    } <= table_names(database_path)
