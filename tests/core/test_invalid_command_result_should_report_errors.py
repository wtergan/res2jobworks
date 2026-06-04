from res2jobworks_core import CommandEnvelope, CommandError


def test_invalid_command_result_should_report_errors() -> None:
    error = CommandError(code="invalid_input", message="job_id is required")

    envelope = CommandEnvelope.failure("jobs.evaluate", errors=[error])

    assert envelope.ok is False
    assert envelope.errors == [error]
