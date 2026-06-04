from res2jobworks_core.seed import seed_public_sample_workspace


def test_fixture_seed_should_create_public_sample_workspace(tmp_path) -> None:
    seeded = seed_public_sample_workspace(tmp_path / "workspace.sqlite3")

    assert seeded["profile"]["id"] == "fixture-profile-jordan-avery"
    assert seeded["resume_source"]["metadata"] == {"fixture": True}
    assert seeded["job"]["id"] == "fixture-job-product-operations-analyst"
    assert seeded["job_source"]["metadata"] == {"fixture": True}
