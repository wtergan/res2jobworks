---
topic: "res2jobWorks project context recovery"
date: 2026-06-03
type: "CODE"
---

## Research Goals

Recover the planning context from the previous Codex session and the current
repo/Vault artifacts so a fresh implementation thread can proceed without
recreating the brainstorm.

## Scope

- Repo paths inspected:
  - `AGENTS.md`
  - `README.md`
  - `.vault/README.md`
  - `.vault/PLAN.md`
  - `.vault/goals/handoff-2026-06-02.md`
- Obsidian notes inspected:
  - `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
  - `/home/gilgames/Vault/01_Projects/res2jobworks/res2jobworks.md`
- Prior session inspected:
  - `/mnt/c/Users/gilgames/.codex/sessions/2026/06/02/rollout-2026-06-02T17-36-09-019e8a43-f147-7a81-8062-3f2b3c53641d.jsonl`
- Related plan:
  - `.vault/PLAN.md`

## Key Findings

### Finding 1: The repo is intentionally planning-only

**Location**: `README.md`
**Tool Used**: `sed`

**Local Implementation**

The README states that implementation scaffolding has not started and that the
next step is to write the first feature plan under `.vault/plans/`.

**Analysis**

The first implementation plan should create the monorepo foundation and not
assume any existing source tree. It should include test harness setup, public
fixtures, command contracts, and docs because no code structure exists yet.

### Finding 2: Project-local instructions lock the architecture boundaries

**Location**: `AGENTS.md`
**Tool Used**: `sed`

**Local Implementation**

`AGENTS.md` requires a public-generic product, monorepo layout, SQLite source of
truth, Markdown/CSV export-only status, core-owned product truth, shared core
contracts for all clients, and no default auto-submit behavior.

**Analysis**

These constraints should be promoted into a durable decision record and repeated
inside every feature plan as boundaries. They are not open implementation
preferences.

### Finding 3: Obsidian notes define the product strategy

**Location**: `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
**Tool Used**: `sed`

**Local Implementation**

The plan supersedes `Res2JobFit`, reframes the product as public-generic and
local-first, and makes evaluation/tracking the first product. It recommends
Python 3.12, `uv`, Typer/Rich, Pydantic, SQLite, Textual, FastAPI, Playwright,
provider adapters, and generated agent wrappers.

**Analysis**

The roadmap can choose Python-first defaults for MVP planning while leaving
specific choices such as SQLAlchemy vs SQLModel and web stack to feature-plan
decision points.

### Finding 4: Previous session created the repo landing pad

**Location**: prior session `019e8a43-f147-7a81-8062-3f2b3c53641d`
**Tool Used**: structured JSONL extraction and `rg`

**Local Implementation**

The previous session renamed `Res2JobFit` to `res2jobWorks`, created the
Obsidian project/plan notes, updated old Vault links, created
`/home/gilgames/Code/res2jobworks`, initialized Git on `main`, and added starter
files plus the `.vault` directory structure.

**Analysis**

The current thread should continue from that handoff by creating durable plans
inside this repo instead of editing the earlier Obsidian notes except for major
strategic rollups.

## Patterns Identified

### Pattern 1: Core-first clients

**Description**: CLI, TUI, web UI, browser automation, and agent wrappers must
be clients over the same core contracts rather than separate sources of product
truth.

**Local Evidence**

- `AGENTS.md` - core owns product truth and all clients share contracts.
- `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md` - command envelope and command registry are central integration surfaces.

**Recommendation**

Plan implementation in layers: core contracts and registry first, SQLite model
second, workflows third, clients/wrappers fourth.

### Pattern 2: Evaluation before generation

**Description**: MVP 1 is evaluation and tracking. Tailoring, cover letters,
and PDF/DOCX generation belong to phase 2.

**Local Evidence**

- `README.md` - planned MVP 1 flow starts with profile/job import, evaluation,
  tracker entry, dashboards, exports, and wrappers.
- `.vault/goals/handoff-2026-06-02.md` - resume tailoring and PDFs are phase 2.

**Recommendation**

Keep phase 2 as a planned but deferred feature plan so future implementation
does not silently expand MVP 1.

## Related Local Artifacts

- Decision: `.vault/decisions/foundational-architecture-2026-06-03.md`
- Visual companion: `.vault/visuals/001-roadmap-architecture-2026-06-03.html`
- Goal run: `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/`

## Recommendations

1. Start with `.vault/plans/001-bootstrap-core-contracts-2026-06-03.md` to create the repo skeleton, command envelope, public fixtures, and test harness.
2. Treat `.vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md` as the first real product-data implementation and require migrations/schema tests.
3. Hold browser automation and document generation until deterministic import/evaluation/export paths are stable.
4. Keep personal dogfooding data out of public fixtures and examples.

## Open Questions

- Should the first web dashboard use FastAPI-rendered templates, React/Vite, SvelteKit, or another local-app approach?
- Should the initial DB layer be SQLAlchemy or SQLModel?
- Should MVP scoring start as deterministic-first, LLM-rubric-first, or a hybrid?
- Should plan 003 include safe URL fetch immediately, or keep first import strictly manual text/file?
