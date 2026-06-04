"""Deterministic cited evaluation workflow for MVP 1."""

import sqlite3
from pathlib import Path
from typing import Any

from res2jobworks_core.commands._support import failure, first_matching_line
from res2jobworks_core.contracts import CommandEnvelope
from res2jobworks_core.repositories.sqlite import RepositoryError, SQLiteRepository

RUBRIC_VERSION = "mvp1-deterministic-v1"


def evaluate_job(
    database_path: Path | str,
    *,
    profile_id: str,
    job_id: str,
    rubric_id: str | None = None,
    evaluation_id: str | None = None,
) -> CommandEnvelope:
    """Evaluate job fit deterministically with source-bound citations."""
    command = "jobs.evaluate"
    inputs = {
        "database_path": str(database_path),
        "profile_id": profile_id,
        "job_id": job_id,
        "rubric_id": rubric_id,
    }
    try:
        if rubric_id is not None and rubric_id != RUBRIC_VERSION:
            raise ValueError(f"unsupported rubric_id: {rubric_id}")
        repository = SQLiteRepository(database_path)
        profile = repository.get_profile(profile_id)
        job = repository.get_job(job_id)
        resume_sources = repository.list_resume_sources(profile_id)
        job_sources = repository.list_job_sources(job_id)
        if not resume_sources:
            raise ValueError("profile must have at least one source before evaluation")
        if not job_sources:
            raise ValueError("job must have at least one source before evaluation")
        result = deterministic_evaluation(
            profile,
            job,
            resume_sources[0],
            job_sources[0],
        )
        resolved_evaluation_id = evaluation_id or f"evaluation-{profile_id}-{job_id}"
        evaluation = repository.create_evaluation(
            evaluation_id=resolved_evaluation_id,
            profile_id=profile_id,
            job_id=job_id,
            rubric_version=RUBRIC_VERSION,
            score=result["score"],
            summary=result["summary"],
            recommendation=result["recommendation"],
            citations=result["citations"],
            provider_kind="deterministic",
            provider_name="res2jobworks-keyword-rubric",
            provider_metadata={
                "rubric_version": RUBRIC_VERSION,
                "dimensions": result["dimensions"],
                "warnings": result["warnings"],
            },
        )
        return CommandEnvelope.success(
            command,
            inputs=inputs,
            data={"evaluation": evaluation, "citations": evaluation["citations"]},
            warnings=result["warnings"],
        )
    except (RepositoryError, sqlite3.Error, ValueError) as exc:
        return failure(command, inputs, exc)


def deterministic_evaluation(
    profile: dict[str, Any],
    job: dict[str, Any],
    resume_source: dict[str, Any],
    job_source: dict[str, Any],
) -> dict[str, Any]:
    """Return cited deterministic rubric output for one profile/job pair."""
    skills = [str(skill).lower() for skill in profile.get("skills", [])]
    job_text = str(job["description"]).lower()
    matched = [skill for skill in skills if skill and skill in job_text]
    skill_score = round((len(matched) / max(len(skills), 1)) * 70)
    communication_bonus = 15 if "communication" in job_text else 0
    evidence_bonus = 15 if "evidence" in job_text or "tracker" in job_text else 0
    score = min(100, skill_score + communication_bonus + evidence_bonus)
    warnings = []
    if not matched:
        warnings.append("no direct skill keyword matches found")
    recommendation = (
        "strong_match"
        if score >= 75
        else "review"
        if score >= 45
        else "weak_match"
    )
    return {
        "score": score,
        "summary": (
            f"Deterministic rubric found {len(matched)} matching profile skills "
            f"for {job['title']}."
        ),
        "recommendation": recommendation,
        "warnings": warnings,
        "dimensions": {
            "matched_skills": matched,
            "skill_score": skill_score,
            "communication_bonus": communication_bonus,
            "evidence_bonus": evidence_bonus,
        },
        "citations": [
            {
                "source_table": "resume_sources",
                "source_id": resume_source["id"],
                "quote": first_matching_line(str(resume_source["content"]), matched),
                "rationale": "Profile evidence used by deterministic rubric.",
            },
            {
                "source_table": "job_sources",
                "source_id": job_source["id"],
                "quote": first_matching_line(str(job_source["content"]), matched),
                "rationale": "Job evidence used by deterministic rubric.",
            },
        ],
    }
