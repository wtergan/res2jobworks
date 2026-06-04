from pathlib import Path

import pytest
from pydantic import ValidationError

from res2jobworks_core import Res2JobWorksConfig


def test_absolute_config_path_should_report_validation_error() -> None:
    with pytest.raises(ValidationError):
        Res2JobWorksConfig(workspace_dir=Path("/home/example/private"))

