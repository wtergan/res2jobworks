"""Draft/fill review plans that explicitly stop before submission."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from res2jobworks_automation.safety import validate_fill_fields
from res2jobworks_core.contracts import CommandEnvelope, CommandError

REQUIRED_REVIEW_STATE = "human_review_required"


@dataclass(frozen=True)
class FillDraft:
    """Reviewed field-draft payload that is not a submit instruction."""

    fields: dict[str, str]
    review_state: str = REQUIRED_REVIEW_STATE


def prepare_fill_review(
    *,
    fields: dict[str, Any],
    review_state: str,
) -> CommandEnvelope:
    """Return fill instructions only when the human-review state is explicit."""
    inputs = {
        "field_count": len(fields),
        "review_state": review_state,
    }
    try:
        normalized_fields = validate_fill_fields(
            {str(key): str(value) for key, value in fields.items()}
        )
    except ValueError as exc:
        return CommandEnvelope.failure(
            "automation.prepare_fill_review",
            inputs=inputs,
            errors=[
                CommandError(
                    code="credential_field_blocked",
                    message=str(exc),
                )
            ],
        )
    if review_state != REQUIRED_REVIEW_STATE:
        return CommandEnvelope.failure(
            "automation.prepare_fill_review",
            inputs=inputs,
            errors=[
                CommandError(
                    code="review_required",
                    message="fill drafts require human_review_required state",
                    field="review_state",
                )
            ],
        )
    return CommandEnvelope.success(
        "automation.prepare_fill_review",
        inputs=inputs,
        data={
            "fill_plan": {
                "fields": normalized_fields,
                "review_state": REQUIRED_REVIEW_STATE,
                "submission_allowed": False,
                "next_action": "review_fields_before_external_action",
            }
        },
        warnings=["default automation stops before submission"],
    )
