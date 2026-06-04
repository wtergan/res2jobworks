---
date: 2026-06-04
related_plan: ".vault/plans/003-import-evaluate-export-workflows-2026-06-03.md"
type: solution
---

# Cited Evaluation Workflow

## Pattern

- Import profile and job sources into SQLite before evaluating.
- Evaluate against stored source rows, not ad hoc text passed directly to the
  evaluator.
- Store deterministic rubric output with `rubric_version`, `provider_kind`,
  provider metadata dimensions, warnings, recommendation, score, and citations.
- Keep citations bound to source rows through repository validation.
- Generate Markdown/CSV exports from SQLite application, job, and evaluation
  rows, then record export metadata as an artifact pointer.

## Verification

Plan 003 workflow tests cover fixture imports, source-bound deterministic
evaluation, append-only application status history, generated Markdown/CSV
exports, private fixture rejection, and export path validation.
