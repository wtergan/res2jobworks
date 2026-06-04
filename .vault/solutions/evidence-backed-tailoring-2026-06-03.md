---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/006-tailoring-documents-phase2-2026-06-03.md"
---

# Evidence-Backed Tailoring Pattern

## Context

Plan 006 adds phase 2 tailoring and document generation after MVP 1 evidence,
evaluation, tracking, client, and browser-capture workflows are stable.

## Pattern

- Build drafts from a single evidence bundle containing profile, resume source,
  job, job source, evaluation, and citations.
- Require every tailoring suggestion and document draft to carry evidence links.
- Keep unsupported requested focus areas as explicit labels instead of silently
  converting them into claims.
- Keep rendered Markdown, DOCX, and PDF files as generated artifacts recorded in
  `exports`; do not mutate canonical profile or job records.
- Expose document workflows through command envelopes and registry-driven CLI
  runners so agent wrappers use the same contracts.

## Boundaries

- No private dogfooding data in fixtures or tests.
- No provider calls in the default deterministic drafting path.
- No generated document submission behavior.
- No rendered artifact is canonical state.

## Verification

- `uv run --extra dev pytest -q tests/documents` -> `8 passed`
- `uv run --extra dev pytest -q` -> `93 passed`
- `uv run --extra dev ruff check .` -> pass
- `uv build` -> built sdist and wheel
- CLI smoke rendered a PDF cover-letter artifact and recorded export metadata.
