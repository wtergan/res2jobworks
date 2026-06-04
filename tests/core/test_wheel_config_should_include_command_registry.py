import tomllib
from pathlib import Path


def test_wheel_config_should_include_command_registry() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    force_include = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"][
        "force-include"
    ]

    assert (
        force_include["commands/registry.yaml"]
        == "packages/core/src/res2jobworks_core/registry.yaml"
    )

