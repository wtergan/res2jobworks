# Goal Handoff

## Resume Here

- Active goal run: `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/`
- Current milestone/task: `M1.T1`
- Current branch/worktree: main branch in `/home/gilgames/Code/res2jobworks`, no implementation branch yet
- Read first:
  - `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/progress.md`
  - `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/task-graph.md`
  - `.vault/PLAN.md`
  - `.vault/plans/001-bootstrap-core-contracts-2026-06-03.md`
  - `.vault/research/project-context-2026-06-03.md`
  - `.vault/decisions/foundational-architecture-2026-06-03.md`

## Latest Known State

The repo is a planning workspace for a public-generic, local-first job-search
workbench. Implementation has not started. The first implementation action is
plan 001: bootstrap the Python-first monorepo, command envelope, config defaults,
starter command registry, public fixtures, docs, and behavior-first tests.

Plans 002-004 form MVP 1: SQLite persistence, import/evaluate/export workflows,
and CLI/TUI/web/agent wrapper interfaces. Plan 005 is safe browser automation
with human review. Plan 006 is deferred phase 2 tailoring and document generation.

## Open Risks

- MVP scope could expand into tailoring before evaluation/tracking is stable.
- Public fixtures could accidentally include private dogfooding data.
- Clients/wrappers could drift from core behavior.
- LLM-backed evaluation could become opaque without citations and versioned rubrics.

## Next Action

Run `$act .vault/plans/001-bootstrap-core-contracts-2026-06-03.md` or paste the native `/goal` contract from `goal.md` to start the long-running MVP implementation loop.
