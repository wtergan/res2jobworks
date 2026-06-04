"""Evidence loading for phase 2 drafting contracts.

Evidence bundles are derived from existing profile, resume source, job source,
and evaluation citation records. They are read models only; SQLite remains the
canonical state owner.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from res2jobworks_core.repositories.sqlite import SQLiteRepository


@dataclass(frozen=True)
class EvidenceLink:
    """A source quote that supports a generated suggestion or draft."""

    source_table: str
    source_id: str
    quote: str
    rationale: str = ""

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready evidence link."""
        return {
            "source_table": self.source_table,
            "source_id": self.source_id,
            "quote": self.quote,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class EvidenceBundle:
    """Canonical records needed to draft with provenance."""

    profile: dict[str, Any]
    resume_source: dict[str, Any]
    job: dict[str, Any]
    job_source: dict[str, Any]
    evaluation: dict[str, Any]
    citations: tuple[EvidenceLink, ...]

    @property
    def provider_matched_skills(self) -> tuple[str, ...]:
        """Return raw provider-reported matches without treating them as claims."""
        metadata = self.evaluation.get("provider_metadata", {})
        dimensions = metadata.get("dimensions", {})
        return tuple(str(skill) for skill in dimensions.get("matched_skills", ()))

    @property
    def verified_profile_skills(self) -> tuple[str, ...]:
        """Return provider matches that are present in stored profile evidence."""
        searchable = _searchable_profile_text(self)
        return tuple(
            skill
            for skill in self.provider_matched_skills
            if _term_in_text(skill, searchable)
        )

    @property
    def unverified_provider_skills(self) -> tuple[str, ...]:
        """Return provider matches that are not supported by profile evidence."""
        verified = set(self.verified_profile_skills)
        return tuple(
            skill for skill in self.provider_matched_skills if skill not in verified
        )


def load_evidence(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None = None,
) -> EvidenceBundle:
    """Load profile/job/evaluation evidence for one drafting context."""
    repository = SQLiteRepository(database_path)
    profile = repository.get_profile(profile_id)
    job = repository.get_job(job_id)
    resume_sources = repository.list_resume_sources(profile_id)
    job_sources = repository.list_job_sources(job_id)
    if not resume_sources:
        raise ValueError("profile must have at least one resume source")
    if not job_sources:
        raise ValueError("job must have at least one job source")
    evaluation = _resolve_evaluation(
        repository,
        profile_id=profile_id,
        job_id=job_id,
        evaluation_id=evaluation_id,
    )
    citations = tuple(
        EvidenceLink(
            source_table=str(citation["source_table"]),
            source_id=str(citation["source_id"]),
            quote=str(citation["quote"]),
            rationale=str(citation.get("rationale", "")),
        )
        for citation in evaluation["citations"]
    )
    return EvidenceBundle(
        profile=profile,
        resume_source=resume_sources[0],
        job=job,
        job_source=job_sources[0],
        evaluation=evaluation,
        citations=citations,
    )


def _resolve_evaluation(
    repository: SQLiteRepository,
    *,
    profile_id: str,
    job_id: str,
    evaluation_id: str | None,
) -> dict[str, Any]:
    if evaluation_id:
        evaluation = repository.get_evaluation(evaluation_id)
        if evaluation["profile_id"] != profile_id or evaluation["job_id"] != job_id:
            raise ValueError("evaluation must match profile_id and job_id")
        return evaluation
    matches = [
        evaluation
        for evaluation in repository.list_evaluations()
        if evaluation["profile_id"] == profile_id and evaluation["job_id"] == job_id
    ]
    if not matches:
        raise ValueError("profile/job pair must be evaluated before drafting")
    return repository.get_evaluation(matches[-1]["id"])


def _searchable_profile_text(evidence: EvidenceBundle) -> str:
    profile_citations = [
        link.quote
        for link in evidence.citations
        if link.source_table in {"profiles", "resume_sources"}
    ]
    return " ".join(
        [
            str(evidence.resume_source["content"]),
            *profile_citations,
        ]
    ).lower()


def _term_in_text(term: str, text: str) -> bool:
    normalized = " ".join(term.lower().split())
    if not normalized:
        return False
    normalized_text = " ".join(text.split())
    pattern = rf"(?<![\w+#.-]){re.escape(normalized)}(?![\w+#.-])"
    return re.search(pattern, normalized_text) is not None
