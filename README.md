# res2jobWorks

`res2jobWorks` is a planned public-generic, local-first job-search workbench.

The project supersedes the earlier `Res2JobFit` idea. Its first product goal is evaluation and tracking: help users decide which jobs deserve attention, explain why with evidence, and keep the application pipeline clean across CLI, TUI, browser UI, and agent workflows.

## Current Status

This repository is a planning workspace. Implementation scaffolding has not started yet.

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

- Vault strategy note: `/home/gilgames/Vault/01_Projects/res2jobworks/res2jobworks.md`
- Vault plan note: `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
- Repo planning index: `.vault/PLAN.md`

## Next Step

Write the first feature plan under `.vault/plans/` for MVP 1: evaluation and tracking.
