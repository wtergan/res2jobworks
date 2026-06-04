---
date: 2026-06-03
status: accepted
related_plan: ".vault/PLAN.md"
---

# ADR: Foundational Architecture

## Context

`res2jobWorks` was created from a previous `Res2JobFit` concept and reframed in
the prior Codex session as a public-generic, local-first job-search workbench.
The repo currently has no implementation code, so the first durable decision
should lock the product and architecture boundaries before scaffolding begins.

Evidence comes from:

- `AGENTS.md`
- `README.md`
- `.vault/PLAN.md`
- `.vault/goals/handoff-2026-06-02.md`
- `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
- `/home/gilgames/Vault/01_Projects/res2jobworks/res2jobworks.md`
- Prior session archive `019e8a43-f147-7a81-8062-3f2b3c53641d`

## Decision

Build `res2jobWorks` as a Python-first monorepo with a local-first core and
SQLite as the canonical source of truth. Markdown, CSV, and JSON are export
formats. CLI, TUI, web UI, browser automation, and agent wrappers are clients
over shared core contracts and a shared command registry. MVP 1 is evaluation
and tracking. Resume tailoring, cover letters, open-ended answer drafting, and
document generation are phase 2. Default behavior must never auto-submit job
applications.

## Drivers

- The product must be public-generic and avoid private user data in default
  fixtures, examples, docs, and templates.
- Local-first storage keeps user job-search data inspectable and user-owned.
- SQLite gives a durable local source of truth without requiring SaaS backend
  setup.
- Core-owned truth prevents drift between CLI, TUI, web dashboard, browser
  automation, and agent integrations.
- Generated agent wrappers let Codex, Hermes, Claude, OpenCode, Gemini, and
  similar tools call the same commands without duplicating product logic.
- Evaluation and tracking are lower-risk foundations for later document
  generation because they establish evidence, citations, and status history.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|---|---|---|---|
| Personal-only assistant over the user's resume and tracker | Fast dogfooding, immediately useful | Bakes private assumptions into product defaults | Conflicts with public-generic identity |
| Markdown/CSV-first tracker | Simple exports and easy manual inspection | Hard to preserve relational history, citations, migrations, and agent runs | Exports should not be canonical data |
| Web-first SaaS architecture | Familiar modern product shape | Adds deployment, auth, data privacy, and hosting scope too early | Conflicts with local-first MVP |
| Separate per-agent implementations | Each agent could feel native | Product logic would drift across tools | Shared registry and CLI/API contracts are more maintainable |
| Resume tailoring as MVP 1 | High user-visible value | Risks opaque generation before evidence/tracking model exists | Evaluation/tracking should prove the data model first |

## Consequences

- Early work must define domain contracts, command envelopes, migrations, and
  tests before feature-heavy UI.
- The first public fixtures need careful sanitization and should not mirror the
  user's private resume or job history.
- Browser automation must stay explicit about human review and should not imply
  autonomous application submission.
- Phase 2 can move faster after MVP 1 because profile, job, evaluation,
  citation, application, and export records will already exist.

## Verification

- Feature plan 001 creates the monorepo foundation, command envelope, and test
  harness.
- Feature plan 002 creates SQLite persistence and schema/migration tests.
- Feature plan 003 proves import, evaluation, citations, status history, and
  exports use SQLite as canonical state.
- Feature plan 004 proves clients and generated wrappers share the same command
  registry.
- Feature plan 005 preserves the no-auto-submit boundary.
- Feature plan 006 starts only after MVP 1 evidence is stable.

## Related Artifacts

- Project index: `.vault/PLAN.md`
- Research: `.vault/research/project-context-2026-06-03.md`
- Research: `.vault/research/predecessor-res2jobfit-and-career-ops-2026-06-03.md`
- Decision: `.vault/decisions/mvp-core-sqlite-source-of-truth-decision-2026-06-03.md`
- Decision: `.vault/decisions/mvp-client-boundaries-decision-2026-06-03.md`
- Decision: `.vault/decisions/mvp-no-autosubmit-default-decision-2026-06-03.md`
- Visual companion: `.vault/visuals/001-roadmap-architecture-2026-06-03.html`
