"""Deterministic evidence-backed tailoring and draft generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from res2jobworks_documents.evidence import EvidenceBundle, EvidenceLink, load_evidence

REVIEW_STATE = "human_review_required"


@dataclass(frozen=True)
class DocumentDraft:
    """A generated document draft that must be reviewed before use."""

    kind: str
    title: str
    body: str
    evidence: tuple[EvidenceLink, ...]
    unsupported_inferences: tuple[str, ...] = ()
    review_state: str = REVIEW_STATE

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready draft."""
        return {
            "kind": self.kind,
            "title": self.title,
            "body": self.body,
            "evidence": [link.to_dict() for link in self.evidence],
            "unsupported_inferences": list(self.unsupported_inferences),
            "review_state": self.review_state,
        }


def build_tailoring_suggestions(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None = None,
) -> list[dict[str, Any]]:
    """Create section-level tailoring suggestions from stored evidence."""
    evidence = load_evidence(
        database_path,
        profile_id=profile_id,
        job_id=job_id,
        evaluation_id=evaluation_id,
    )
    unsupported = evidence.unverified_provider_skills
    skills = ", ".join(evidence.verified_profile_skills) or "the cited profile evidence"
    original = _first_nonempty_line(str(evidence.resume_source["content"]))
    proposed = (
        f"Emphasize {skills} for the {evidence.job['title']} role while keeping "
        "the original profile claims intact."
    )
    return [
        {
            "section": "summary",
            "original": original,
            "proposed": proposed,
            "rationale": evidence.evaluation["summary"],
            "evidence": [link.to_dict() for link in evidence.citations],
            "unsupported_inferences": list(unsupported),
            "review_state": REVIEW_STATE,
        }
    ]


def build_resume_diff(suggestion: dict[str, Any]) -> dict[str, Any]:
    """Return a reversible section-level resume diff for human review."""
    return {
        "section": suggestion["section"],
        "original": suggestion["original"],
        "proposed": suggestion["proposed"],
        "rationale": suggestion["rationale"],
        "evidence": suggestion["evidence"],
        "review_state": REVIEW_STATE,
        "reversible": True,
    }


def build_cover_letter_draft(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None = None,
    requested_focus: tuple[str, ...] = (),
) -> DocumentDraft:
    """Draft a cover letter from stored evidence and labeled gaps."""
    evidence = load_evidence(
        database_path,
        profile_id=profile_id,
        job_id=job_id,
        evaluation_id=evaluation_id,
    )
    unsupported = _combine_unsupported(
        evidence.unverified_provider_skills,
        _unsupported_focus(evidence, requested_focus),
    )
    skills = ", ".join(evidence.verified_profile_skills) or "the cited experience"
    body = "\n\n".join(
        [
            f"Dear {evidence.job['employer']} team,",
            (
                f"I am interested in the {evidence.job['title']} role. "
                f"My stored profile evidence supports emphasis on {skills}."
            ),
            (
                "The strongest support comes from the cited resume and job-source "
                "records listed in the provenance section."
            ),
            _unsupported_sentence(unsupported),
        ]
    )
    return DocumentDraft(
        kind="cover_letter",
        title=f"Cover letter draft for {evidence.job['title']}",
        body=body,
        evidence=evidence.citations,
        unsupported_inferences=unsupported,
    )


def build_application_answer_draft(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    question: str,
    evaluation_id: str | None = None,
) -> DocumentDraft:
    """Draft an application answer and label weakly supported requests."""
    evidence = load_evidence(
        database_path,
        profile_id=profile_id,
        job_id=job_id,
        evaluation_id=evaluation_id,
    )
    unsupported = _combine_unsupported(
        evidence.unverified_provider_skills,
        _unsupported_focus(evidence, tuple(question.split())),
    )
    skills = ", ".join(evidence.verified_profile_skills) or "the cited profile evidence"
    body = (
        f"Question: {question}\n\n"
        "Answer draft: Based on the stored evidence, emphasize "
        f"{skills}."
    )
    if unsupported:
        body += "\n\nUnsupported inference labels: " + ", ".join(unsupported)
    return DocumentDraft(
        kind="application_answer",
        title="Application answer draft",
        body=body,
        evidence=evidence.citations,
        unsupported_inferences=unsupported,
    )


def _unsupported_focus(
    evidence: EvidenceBundle,
    requested_focus: tuple[str, ...],
) -> tuple[str, ...]:
    searchable = " ".join(
        [
            str(evidence.resume_source["content"]),
            str(evidence.job_source["content"]),
        ]
    ).lower()
    unsupported = []
    for focus in requested_focus:
        normalized = focus.strip().lower()
        if len(normalized) < 4:
            continue
        if normalized not in searchable:
            unsupported.append(focus)
    return tuple(dict.fromkeys(unsupported))


def _combine_unsupported(
    *groups: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(dict.fromkeys(item for group in groups for item in group))


def _unsupported_sentence(unsupported: tuple[str, ...]) -> str:
    if not unsupported:
        return "No unsupported focus areas were added to this draft."
    return "Unsupported inference labels: " + ", ".join(unsupported)


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip(" -#")
        if stripped:
            return stripped
    return ""
