# Goal Task Graph

## Milestones

### M1: Foundation

- Goal: Establish monorepo shape, core contracts, command envelope, registry, fixtures, docs, and test harness.
- Depends on: None
- Validation level: L2 targeted suite
- Review gate: pre-merge

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M1.T1 | `.vault/plans/001-bootstrap-core-contracts-2026-06-03.md` | Bootstrap monorepo and core contracts | complete | None | implementer | `pytest -q`, `ruff check .` |

### M2: SQLite Source of Truth

- Goal: Create canonical local persistence and migration/repository patterns.
- Depends on: M1
- Validation level: L2 targeted suite
- Review gate: pre-merge

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M2.T1 | `.vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md` | Build SQLite schema, migrations, and repositories | ready | M1.T1 | implementer | `pytest -q tests/db`, `pytest -q` |

### M3: MVP Workflows

- Goal: Implement import, cited evaluation, application tracking, and exports.
- Depends on: M2
- Validation level: L3 workflow gate
- Review gate: pre-merge

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M3.T1 | `.vault/plans/003-import-evaluate-export-workflows-2026-06-03.md` | Build import/evaluate/export workflows | planned | M2.T1 | implementer | `pytest -q tests/workflows`, `pytest -q` |

### M4: Interfaces

- Goal: Expose equivalent behavior through CLI, TUI, web dashboard, and generated wrappers.
- Depends on: M3
- Validation level: L3 client parity gate
- Review gate: pre-merge

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M4.T1 | `.vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md` | Build clients and generated wrappers | planned | M3.T1 | implementer/design-iterator | `pytest -q tests/parity`, browser/accessibility checks |

### M5: Automation Follow-Up

- Goal: Add browser source capture and draft/fill/review support without default auto-submit.
- Depends on: M3, M4
- Validation level: L3 safety gate
- Review gate: pre-merge and security review

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M5.T1 | `.vault/plans/005-browser-automation-human-review-2026-06-03.md` | Add safe browser automation | planned | M3.T1, M4.T1 | implementer/security | `pytest -q tests/automation tests/security` |

### M6: Phase 2 Documents

- Goal: Add evidence-backed tailoring and document generation after MVP 1 stabilizes.
- Depends on: M3, M4, preferably M5
- Validation level: L3 provenance gate
- Review gate: pre-merge and security review

| Task ID | Plan | Task | State | Depends On | Owner/Lane | Validation |
|---|---|---|---|---|---|---|
| M6.T1 | `.vault/plans/006-tailoring-documents-phase2-2026-06-03.md` | Implement phase 2 documents | planned | M3.T1, M4.T1 | implementer/security | `pytest -q tests/documents` |

## State Values

- planned
- ready
- in_progress
- verifying
- review_pending
- blocked
- complete
- ready_next
