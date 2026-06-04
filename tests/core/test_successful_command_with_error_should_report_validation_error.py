import pytest
from pydantic import ValidationError

from res2jobworks_core import CommandEnvelope, CommandError


def test_successful_command_with_error_should_report_validation_error() -> None:
    with pytest.raises(ValidationError):
        CommandEnvelope(
            ok=True,
            command="jobs.evaluate",
            errors=[CommandError(code="unexpected", message="should not happen")],
        )

