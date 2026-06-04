# res2jobWorks AGENTS

## Project Identity

`res2jobWorks` is public-generic from day one. Do not build around one user's private resume, tracker, or application history as the product default.

Use personal workflow only as a dogfooding path. Public examples, fixtures, docs, and templates must avoid private personal data.

## Planning First Reads

Before substantive work, read:

- `.vault/PLAN.md`
- `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
- `/home/gilgames/Vault/01_Projects/res2jobworks/res2jobworks.md`

## Architecture Decisions

- Use a monorepo layout when implementation starts.
- SQLite is the canonical source of truth.
- Markdown and CSV are export formats, not the primary data store.
- Core owns product truth.
- CLI, TUI, web UI, browser automation, and agent skills are clients over the same core contracts.
- MVP 1 is evaluation and tracking.
- Resume tailoring, cover letters, and document generation are phase 2.
- Default behavior must never auto-submit job applications.

## Repo Memory

Use `.vault/` for active engineering memory:

- `.vault/PLAN.md` for the project index
- `.vault/plans/` for executable feature plans
- `.vault/research/` for code and external research
- `.vault/decisions/` for durable decisions
- `.vault/solutions/` for reusable implementation patterns
- `.vault/encounters/` for reusable failure/blocker notes
- `.vault/goals/` for long-running goal state
- `.vault/visuals/` for diagrams and visual companions

Keep Obsidian notes strategic and human-facing. Keep implementation detail in this repo's `.vault/`.

## Implementation Guardrails

- Keep the core local-first and inspectable.
- Prefer deterministic parsing, persistence, export, and validation where practical.
- Make LLM-backed evaluation cited, reversible, and clearly labeled.
- Generate agent wrappers from a shared command registry instead of duplicating product logic.
- Keep TUI and web dashboard behavior equivalent over the same backend/data model.
