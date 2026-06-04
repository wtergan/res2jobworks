from res2jobworks_automation import prepare_fill_review


def test_fill_draft_should_require_human_review_state() -> None:
    blocked = prepare_fill_review(
        fields={"full_name": "Jordan Avery"},
        review_state="ready_to_submit",
    )
    allowed = prepare_fill_review(
        fields={"full_name": "Jordan Avery"},
        review_state="human_review_required",
    )

    assert not blocked.ok
    assert blocked.errors[0].code == "review_required"
    assert allowed.ok
    assert allowed.data["fill_plan"]["submission_allowed"] is False
