# Goal: MVP Evaluation and Tracking

## Objective

Coordinate the first implementation arc for `res2jobWorks`: bootstrap the
monorepo, implement SQLite-backed evaluation/tracking, build import/evaluate/export
workflows, and expose the workflow through CLI, TUI, web dashboard, and generated
agent wrappers.

## Starting Point

- Project index: `.vault/PLAN.md`
- Active goal run: `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/`
- Existing plans:
  - `.vault/plans/001-bootstrap-core-contracts-2026-06-03.md`
  - `.vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md`
  - `.vault/plans/003-import-evaluate-export-workflows-2026-06-03.md`
  - `.vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md`
  - `.vault/plans/005-browser-automation-human-review-2026-06-03.md`
  - `.vault/plans/006-tailoring-documents-phase2-2026-06-03.md`

## Acceptance Criteria

- [ ] Plans 001-004 are complete with focused and broad verification evidence.
- [ ] SQLite is canonical for profiles, jobs, evaluations, citations, applications, status history, notes, exports, and agent runs.
- [ ] Markdown and CSV exports are generated artifacts from SQLite.
- [ ] CLI, TUI, web dashboard, and generated wrappers share core behavior and command envelopes.
- [ ] Public examples and fixtures contain no private personal data.
- [ ] Browser automation and phase 2 documents remain follow-up scope unless explicitly activated.

## Non-Goals and Approval Boundaries

- Do not auto-submit applications.
- Do not add private dogfooding data to public fixtures, examples, or docs.
- Do not start document generation before MVP 1 is stable.
- Ask before adding paid services, live provider calls in tests, credentials, hosted deployment, or browser behavior involving real sites.

## Constraints

- Public-generic from day one.
- Local-first by default.
- Core owns product truth.
- All clients call shared core contracts.
- LLM-backed evaluation must be cited, reversible, and clearly labeled.
- Behavior changes should use TDD where practical.

## Native Goal Contract

```text
/goal Outcome: Build res2jobWorks MVP 1 through the linked plans so a public-generic local-first job-search workbench can initialize a workspace, import profile/job data, evaluate with citations, track applications in SQLite, export Markdown/CSV, and expose equivalent CLI/TUI/web/agent-wrapper workflows. Context: start from `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/handoff.md`, `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/task-graph.md`, `.vault/PLAN.md`, and plans 001-004. Boundaries: no private fixture data, no default auto-submit, no SaaS backend, no phase 2 document generation unless explicitly approved. Verify with focused tests per plan, full `pytest -q`, `ruff check .`, client parity checks, and browser/accessibility checks for web UI. Iterate in small milestones, update progress after each meaningful action, capture decisions/solutions/encounters when durable, and stop for approval boundaries or repeated blockers. Done when plans 001-004 are complete with evidence and plans 005-006 are either still deferred or separately activated.
```
