from res2jobworks_core.commands import import_profile


def test_private_fixture_import_should_report_validation_error(tmp_path) -> None:
    envelope = import_profile(
        tmp_path / "workspace.sqlite3",
        source_text="name: Example\napi_key: live-secret\n",
        source_type="yaml_fixture",
    )

    assert not envelope.ok
    assert envelope.errors[0].code == "ValueError"
    assert "not public-generic" in envelope.errors[0].message
