import tomllib
from pathlib import Path


def test_wheel_config_should_include_seed_fixtures() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    force_include = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"][
        "force-include"
    ]

    assert (
        force_include["templates/profile-example.yaml"]
        == "res2jobworks_core/fixtures/profile-example.yaml"
    )
    assert (
        force_include["examples/jobs/sample-job.md"]
        == "res2jobworks_core/fixtures/sample-job.md"
    )
