# res2jobWorks

`res2jobWorks` is a public-generic, local-first job-search workbench.

The project supersedes the earlier `Res2JobFit` idea. Its first product goal is evaluation and tracking: help users decide which jobs deserve attention, explain why with evidence, and keep the application pipeline clean across CLI, TUI, browser UI, and agent workflows.

## Current Status

Bootstrap implementation has started. The repo now has a Python-first monorepo
scaffold, a core package with shared command contracts, public fixtures, a
starter command registry, and behavior-first tests.

Run the current bootstrap checks with:

```bash
uv run --extra dev pytest -q
uv run --extra dev ruff check .
uv run python -m res2jobworks_core
```

## Locked Direction

- Public-generic from day one.
- Monorepo layout from the first implementation.
- SQLite is the source of truth.
- Markdown and CSV are export formats.
- MVP 1 prioritizes evaluation and tracking.
- Resume tailoring and PDF/DOCX generation are phase 2.
- Agents, TUI, and web UI are clients; the core owns product truth.
- Default product behavior never auto-submits applications.

## Planned MVP 1

```text
public setup
-> profile/resume import
-> job/JD import
-> evaluation with citations
-> tracker entry in SQLite
-> TUI dashboard
-> web dashboard
-> Markdown/CSV exports
-> generated agent wrappers
```

## Planning References

- Feature plans: `.vault/plans/`
- Architecture decisions: `.vault/decisions/`
- Public fixture policy: `docs/fixtures.md`
- Repo planning index: `.vault/PLAN.md`

## Next Step

Implement the SQLite evaluation/tracking model in
`.vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md`.
