# res2jobWorks

`res2jobWorks` is a public-generic, local-first job-search workbench.

The project supersedes the earlier `Res2JobFit` idea. Its first product goal is evaluation and tracking: help users decide which jobs deserve attention, explain why with evidence, and keep the application pipeline clean across CLI, TUI, browser UI, and agent workflows.

## Current Status

Plans 001-006 are implemented. The repo has a Python-first monorepo scaffold,
SQLite-backed core workflows, public fixtures, CLI/TUI/web client surfaces,
generated agent-wrapper contracts, safe browser capture/fill-review helpers,
and evidence-backed phase 2 document generation.

Run the current checks with:

```bash
uv run --extra dev pytest -q
uv run --extra dev ruff check .
uv build
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

## Implemented Workflow

```text
workspace init
-> profile/resume import
-> job/JD import
-> evaluation with citations
-> tracker entry in SQLite
-> TUI dashboard
-> web dashboard
-> Markdown/CSV exports
-> safe browser capture/fill review
-> evidence-backed document drafts and artifacts
-> generated agent wrappers
```

## Planning References

- Feature plans: `.vault/plans/`
- Architecture decisions: `.vault/decisions/`
- Public fixture policy: `docs/fixtures.md`
- Repo planning index: `.vault/PLAN.md`

## Next Step

Use `.vault/PLAN.md` and the completed feature plans in `.vault/plans/` as the
current engineering index. Preserve the documented SQLite source-of-truth,
public-generic fixture, and no-default-auto-submit boundaries when extending the
product.
