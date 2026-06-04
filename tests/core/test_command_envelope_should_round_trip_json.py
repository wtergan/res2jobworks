from res2jobworks_core import CommandEnvelope


def test_command_envelope_should_round_trip_json() -> None:
    envelope = CommandEnvelope.success(
        "jobs.evaluate",
        inputs={"job_id": "job_fixture"},
        data={"score": 82},
        files=["exports/evaluation.md"],
        warnings=["fixture evaluation"],
    )

    serialized = envelope.model_dump_json()
    loaded = CommandEnvelope.model_validate_json(serialized)

    assert loaded == envelope
    assert loaded.ok is True
    assert loaded.command == "jobs.evaluate"

