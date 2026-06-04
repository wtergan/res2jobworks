"""Deterministic ATS/readability checks for generated drafts."""

from __future__ import annotations

import re

from res2jobworks_documents.drafting import DocumentDraft


def analyze_document_readiness(
    draft: DocumentDraft,
    *,
    target_keywords: tuple[str, ...] = (),
) -> dict:
    """Return labeled local checks for review, ATS, and readability signals."""
    sentences = [item for item in re.split(r"[.!?]+", draft.body) if item.strip()]
    words = re.findall(r"\b\w+\b", draft.body)
    average_sentence_length = len(words) / max(len(sentences), 1)
    lowered_body = draft.body.lower()
    matched_keywords = [
        keyword for keyword in target_keywords if keyword.lower() in lowered_body
    ]
    coverage = len(matched_keywords) / max(len(target_keywords), 1)
    return {
        "draft_kind": draft.kind,
        "checks": [
            {
                "name": "readability.average_sentence_length",
                "method": "deterministic",
                "label": "local deterministic check",
                "value": round(average_sentence_length, 2),
                "status": "review" if average_sentence_length > 28 else "ok",
            },
            {
                "name": "ats.keyword_coverage",
                "method": "deterministic",
                "label": "local deterministic check",
                "value": round(coverage, 2),
                "matched_keywords": matched_keywords,
                "missing_keywords": [
                    keyword
                    for keyword in target_keywords
                    if keyword not in matched_keywords
                ],
                "status": "review" if coverage < 1 else "ok",
            },
        ],
    }
