from res2jobworks_core.fixtures import validate_public_fixture_text


def test_fixture_with_auth_material_should_report_private_marker() -> None:
    result = validate_public_fixture_text(
        """
fictional fixture
Authorization: Bearer live-token-value
cookie: sessionid=abc123
access_token=abc123
"""
    )

    assert not result.ok
    assert result.errors

