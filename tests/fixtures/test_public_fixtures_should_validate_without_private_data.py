from pathlib import Path

from res2jobworks_core.fixtures import (
    discover_public_fixture_files,
    validate_public_fixture_files,
)


def test_public_fixtures_should_validate_without_private_data() -> None:
    fixture_paths = discover_public_fixture_files(
        [
            Path("templates"),
            Path("examples"),
        ]
    )

    assert fixture_paths
    result = validate_public_fixture_files(fixture_paths)

    assert result.ok, result.errors
