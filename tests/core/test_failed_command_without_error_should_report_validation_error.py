import pytest
from pydantic import ValidationError

from res2jobworks_core import CommandEnvelope


def test_failed_command_without_error_should_report_validation_error() -> None:
    with pytest.raises(ValidationError):
        CommandEnvelope(ok=False, command="jobs.evaluate")

