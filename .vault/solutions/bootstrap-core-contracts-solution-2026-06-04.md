---
date: 2026-06-04
related_plan: ".vault/plans/001-bootstrap-core-contracts-2026-06-03.md"
type: solution
---

# Bootstrap Core Contracts Solution

## Context

Plan 001 needed the first implementation scaffold without crossing into
persistence, UI, browser automation, providers, or document generation.

## Pattern

- Keep the root `pyproject.toml` as the project entrypoint and package only the
  core source tree for now.
- Keep client and follow-on package folders as documented placeholders until
  their feature plans implement behavior.
- Put the shared command metadata in `commands/registry.yaml` and validate it
  through `res2jobworks_core.registry`.
- Package the shared registry into the wheel as
  `res2jobworks_core/registry.yaml` and load it with `importlib.resources`.
  Source-tree discovery is allowed for local development; current-working-
  directory discovery is not an implicit fallback.
- Return command outcomes through `CommandEnvelope` with explicit errors on
  failure; do not allow success-shaped failed envelopes.
- Keep config defaults relative, local-first, and provider-disabled.
- Ignore `.res2jobworks/` wholesale so local dogfooding workspaces do not become
  commit-visible.
- Validate public fixtures with conservative marker scans before they become
  seed data for later plans.

## Verification

- `uv run --extra dev pytest -q` -> `13 passed`
- `uv run --extra dev ruff check .` -> `All checks passed!`
- `uv run python -m res2jobworks_core` -> `res2jobworks-core ok workspace=.res2jobworks`
- `uv build` -> built sdist and wheel
- Fresh installed wheel check from `/tmp` -> `jobs.evaluate`
