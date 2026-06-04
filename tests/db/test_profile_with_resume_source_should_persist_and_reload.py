from res2jobworks_core.repositories.sqlite import SQLiteRepository


def test_profile_with_resume_source_should_persist_and_reload(tmp_path) -> None:
    repository = SQLiteRepository(tmp_path / "workspace.sqlite3")

    profile = repository.create_profile(
        profile_id="profile-1",
        display_name="Fictional User",
        headline="Example operator",
        summary="Fixture profile",
        skills=["workflow", "sql"],
    )
    source = repository.add_resume_source(
        source_id="resume-source-1",
        profile_id=profile["id"],
        source_type="yaml_fixture",
        title="profile-example.yaml",
        content="fictional fixture profile",
    )
    reloaded = repository.get_profile("profile-1")

    assert reloaded["display_name"] == "Fictional User"
    assert reloaded["skills"] == ["workflow", "sql"]
    assert source["profile_id"] == "profile-1"
