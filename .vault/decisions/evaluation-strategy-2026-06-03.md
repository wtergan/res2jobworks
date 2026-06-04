---
date: 2026-06-04
status: accepted
related_plan: ".vault/plans/003-import-evaluate-export-workflows-2026-06-03.md"
---

# ADR: MVP Evaluation Strategy

## Context

Plan 003 needs job-fit evaluation records that are useful before live provider
integration exists. Project guardrails require evaluation output to be cited,
versioned, reversible, and testable without credentials.

## Decision

Use a deterministic-first rubric evaluator for MVP 1. The evaluator compares
stored profile skills and source text against stored job descriptions, creates a
bounded score, records warnings and rubric metadata in provider metadata, and
stores citations tied to the profile and job source records.

LLM-backed providers remain a later adapter path. When added, they must write
the same repository evaluation shape: rubric version, provider kind/name,
safe provider metadata, recommendation, warnings, and source-bound citations.

## Drivers

- Default tests must run without live credentials or network access.
- Users need inspectable evidence before trusting generated recommendations.
- SQLite remains canonical; exports are derived from stored evaluations.
- Deterministic records give CLI, TUI, web, and agent wrappers the same contract
  before provider-specific behavior exists.

## Consequences

- MVP scores are intentionally conservative and transparent rather than
  pretending to be a full hiring prediction.
- Provider metadata stores rubric dimensions and warnings, not secrets.
- Future LLM adapters can be introduced behind the same workflow contract.

## Verification

- `uv run --extra dev pytest -q tests/workflows`
- `uv run --extra dev pytest -q`
- `uv run --extra dev ruff check .`
