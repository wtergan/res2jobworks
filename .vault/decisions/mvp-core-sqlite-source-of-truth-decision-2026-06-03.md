---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md"
---

# ADR: MVP Core SQLite Source of Truth

## Context

`res2jobWorks` needs durable local state for profiles, resume sources, jobs, job
sources, evaluations, citations, applications, status history, notes, exports,
and agent runs. The prior session and project instructions repeatedly state
that SQLite is canonical and Markdown/CSV are exports.

## Decision

Use SQLite as the MVP source of truth. Markdown, CSV, JSON, PDF, DOCX, and other
generated files are artifacts derived from canonical records and must point back
to the records they summarize or render.

## Drivers

- Local-first ownership and inspectability.
- Relational integrity for citations and application history.
- Durable status events that can be queried and exported.
- Stable backend for CLI, TUI, web, automation, and agent wrappers.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|---|---|---|---|
| Markdown-first tracker | Easy to inspect and edit | Weak relational integrity and migration story | Better as export format |
| CSV-first tracker | Familiar application tracker shape | Loses nested evaluation/citation structure | Better as export format |
| JSON files | Simple local storage | Harder to query, migrate, and preserve relationships | Acceptable as envelope/export, not canonical DB |
| Hosted database | Powerful and scalable | Adds auth, deployment, privacy, and cost scope | Contradicts local-first MVP |

## Consequences

- Plan 002 must create migrations and repository tests before workflows depend
  on persistence.
- Exports must be generated from SQLite and recorded in export metadata.
- Future document artifacts must preserve provenance to canonical records.

## Verification

- `pytest -q tests/db` after plan 002.
- Workflow tests in plan 003 prove exports are generated from SQLite.
- Client parity tests in plan 004 prove clients use core commands rather than
  reading export files as truth.

## Related Artifacts

- Plan: `.vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md`
- Research: `.vault/research/project-context-2026-06-03.md`
