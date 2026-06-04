from res2jobworks_automation import prepare_fill_review


def test_fill_review_should_reject_credential_fields() -> None:
    envelope = prepare_fill_review(
        fields={"password": "live-password", "full_name": "Jordan Avery"},
        review_state="human_review_required",
    )

    serialized = envelope.model_dump_json()
    assert not envelope.ok
    assert envelope.errors[0].code == "credential_field_blocked"
    assert "live-password" not in serialized
