from res2jobworks_core import load_config


def test_default_config_should_avoid_private_paths() -> None:
    config = load_config()

    assert not config.workspace_dir.is_absolute()
    assert not config.data_dir.is_absolute()
    assert not config.exports_dir.is_absolute()
    assert str(config.database_path) == ".res2jobworks/data/res2jobworks.sqlite3"
    assert config.enable_provider_calls is False
