from pathlib import Path

from res2jobworks_core.fixtures import discover_public_fixture_files


def test_fixture_discovery_should_include_nested_public_examples() -> None:
    fixture_paths = discover_public_fixture_files(
        [
            Path("templates"),
            Path("examples"),
        ]
    )

    assert Path("templates/profile-example.yaml") in fixture_paths
    assert Path("examples/jobs/sample-job.md") in fixture_paths

