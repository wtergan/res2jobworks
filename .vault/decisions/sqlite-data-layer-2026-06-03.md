---
date: 2026-06-04
status: accepted
related_plan: ".vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md"
---

# ADR: SQLite Data Layer

## Context

Plan 002 needs canonical local persistence for MVP 1 evaluation and tracking.
The project direction requires SQLite as the source of truth, export formats as
generated artifacts, and clients over core contracts.

## Decision

Use Python's standard-library `sqlite3` module with explicit SQL migrations
packaged inside `res2jobworks_core.db.migrations`. Repositories expose typed,
validation-heavy methods and return decoded dictionaries rather than leaking raw
SQLite rows or ORM objects.

## Drivers

- SQLite is the canonical local state and should remain easy to inspect.
- MVP 1 schema and repository contracts are still stabilizing.
- A lightweight migration runner avoids introducing ORM/Alembic complexity
  before workflow and client layers prove they need it.
- Package-contained migrations support installed CLI and agent wrappers without
  requiring a source checkout.

## Consequences

- SQL remains explicit and reviewable.
- Repository methods must carry validation and transaction boundaries.
- Future plans may add SQLAlchemy or Alembic if query complexity or migration
  volume outgrows the lightweight runner.

## Verification

- `uv run --extra dev pytest -q tests/db`
- `uv run --extra dev pytest -q`
- `uv run --extra dev ruff check .`
