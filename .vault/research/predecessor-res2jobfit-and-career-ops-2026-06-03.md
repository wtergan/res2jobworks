---
topic: "Res2JobFit and career-ops predecessor research"
date: 2026-06-03
type: "CODE"
---

## Research Goals

Capture usable inheritance from the predecessor `Res2JobFit` workspace and the
local `career-ops` resource note without letting resume tailoring, PDF export,
ATS scoring, or Claude-specific workflow become the new MVP.

## Scope

- Repo paths inspected:
  - `/home/gilgames/Code/Res2JobFit/README.md`
  - `/home/gilgames/Code/Res2JobFit/Res2JobFit-Plan.md`
  - `/home/gilgames/Code/Res2JobFit/commands/registry.yaml`
  - `/home/gilgames/Code/Res2JobFit/docs/agent-commands.md`
  - `/home/gilgames/Code/Res2JobFit/pyproject.toml`
  - `/home/gilgames/Code/Res2JobFit/src/res2jobfit/cli.py`
- Vault resources inspected:
  - `/home/gilgames/Vault/03_Resources/repositories/ai-agent-runtimes-workflows/santifer-career-ops-3dfbecc2.md`
  - `/home/gilgames/Vault/02_Areas/Career/Res2JobWorks-Plan.md`
- Related plan:
  - `.vault/PLAN.md`

## Key Findings

### Finding 1: Res2JobFit already explored CLI-first agent interoperability

**Location**: `/home/gilgames/Code/Res2JobFit/README.md`
**Tool Used**: `sed`

**Local Implementation**

The predecessor described a Python CLI designed for Codex, OpenCode, manual use,
and deterministic JSON outputs. It explicitly positioned slash commands as thin
wrappers over CLI commands.

**Analysis**

This should be retained in `res2jobWorks`: the shared command registry and JSON
envelope should be foundational. The new project should rename and broaden the
contract around evaluation/tracking rather than copy the resume-generation-first
command set.

### Finding 2: The predecessor registry is useful as a pattern, not a command list

**Location**: `/home/gilgames/Code/Res2JobFit/commands/registry.yaml`
**Tool Used**: `sed`

**Local Implementation**

The old registry included `resume-tailor`, `resume-score`, `cover-letter`,
`jd-analyze`, `jobs-find`, and `track-add` entries with CLI templates and JSON
or file outputs.

**Analysis**

The registry shape is useful, but the command priorities should change. MVP 1
should start with workspace/profile/job import, job evaluation, application
tracking, exports, and wrapper generation. Tailoring, cover letters, ATS/PDF
output, and batch generation belong to phase 2.

### Finding 3: The predecessor stack is heavier than MVP 1 needs

**Location**: `/home/gilgames/Code/Res2JobFit/pyproject.toml`
**Tool Used**: `sed`

**Local Implementation**

The old project depended on document, parsing, privacy, provider, scoring, and
data packages including `python-docx`, `pdfplumber`, `trafilatura`, `pandas`,
`openpyxl`, `presidio`, and optional scoring/provider extras.

**Analysis**

Plan 001 should start with only the dependencies needed for core contracts,
tests, config, and CLI scaffolding. Heavier document/scoring/provider packages
should be added only when a feature plan needs them.

### Finding 4: career-ops is inspiration, not architecture authority

**Location**: `/home/gilgames/Vault/03_Resources/repositories/ai-agent-runtimes-workflows/santifer-career-ops-3dfbecc2.md`
**Tool Used**: `sed`

**Local Implementation**

The local note summarizes `career-ops` as a Claude Code-powered job-search
system with skill modes, dashboard, PDF generation, and batch processing, while
also warning that the note is an Inbox capture rather than canonical resource.

**Analysis**

`career-ops` can inspire workflow breadth and agent ergonomics, but
`res2jobWorks` should stay agent-agnostic, local-first, public-generic, and
core-contract-driven.

## Patterns Identified

### Pattern 1: Registry-driven agent wrappers

**Description**: Store command metadata once, then generate agent-specific
wrappers or manifests.

**Local Evidence**

- `/home/gilgames/Code/Res2JobFit/docs/agent-commands.md` describes slash
  commands as thin wrappers over registry CLI templates.
- `/home/gilgames/Code/Res2JobFit/commands/registry.yaml` stores command ids,
  descriptions, inputs, and outputs.

**Recommendation**

Keep the registry in plan 001, validate it with tests, and make plan 004's
wrappers generated from the registry rather than hand-written product logic.

### Pattern 2: Deterministic flows should not require providers

**Description**: The old plan says deterministic parsing/scoring can run without
LLMs and LLM-backed rewriting should degrade with clear warnings.

**Local Evidence**

- `/home/gilgames/Code/Res2JobFit/docs/agent-commands.md`
- `/home/gilgames/Code/Res2JobFit/Res2JobFit-Plan.md`

**Recommendation**

For `res2jobWorks`, deterministic import, tracking, export, and local tests must
work without provider credentials. LLM-backed evaluation should be optional,
cited, reversible, and gracefully unavailable.

## Related Local Artifacts

- Decisions:
  - `.vault/decisions/foundational-architecture-2026-06-03.md`
  - `.vault/decisions/mvp-client-boundaries-decision-2026-06-03.md`
- Plans:
  - `.vault/plans/001-bootstrap-core-contracts-2026-06-03.md`
  - `.vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md`
  - `.vault/plans/006-tailoring-documents-phase2-2026-06-03.md`

## Recommendations

1. Reuse the predecessor's CLI, registry, and wrapper posture.
2. Do not reuse the old command priorities as MVP 1 priorities.
3. Keep provider, document, ATS, and PDF dependencies out of the core bootstrap unless a later plan proves they are needed.
4. Treat `career-ops` as inspiration and research input, not a template to clone.

## Open Questions

- Which agent wrapper format should be generated first after the CLI contract is stable?
- Should any old `Res2JobFit` registry fields be preserved verbatim, or should the new registry schema start fresh?
- Should `career-ops` be cloned under `/home/gilgames/Code/github-clones/` for deeper research before plan 004?
