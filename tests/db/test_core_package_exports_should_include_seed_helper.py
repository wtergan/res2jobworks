from res2jobworks_core import seed_public_sample_workspace


def test_core_package_exports_should_include_seed_helper() -> None:
    assert callable(seed_public_sample_workspace)
