from res2jobworks_core.commands import export_applications


def test_export_with_absolute_path_should_report_validation_error(tmp_path) -> None:
    envelope = export_applications(
        tmp_path / "workspace.sqlite3",
        output_path=tmp_path / "tracker.md",
        format="markdown",
    )

    assert not envelope.ok
    assert "output_path must be relative" in envelope.errors[0].message
