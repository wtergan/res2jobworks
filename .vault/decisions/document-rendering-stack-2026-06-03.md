---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/006-tailoring-documents-phase2-2026-06-03.md"
---

# ADR: Document Rendering Stack

## Context

Phase 2 document generation must produce useful artifacts without weakening the
MVP 1 evidence model. Rendering dependencies can easily dominate the scope, and
generated documents are high-risk if they imply unsupported resume claims.

## Decision

Use a Markdown-first rendering stack for Plan 006. Implement deterministic
stdlib renderers for Markdown, minimal DOCX, and minimal PDF artifacts behind a
shared document renderer interface. Defer richer `python-docx`, WeasyPrint, and
Pandoc adapters until evidence-backed drafting and artifact metadata are stable.

## Drivers

- Markdown is inspectable, diffable, and already part of the repo's export
  story.
- The default product should not require native PDF dependencies or external
  binaries.
- DOCX/PDF support should be structurally testable before styling is optimized.
- SQLite remains canonical; rendered documents are recorded exports.
- Human review and provenance are more important than visual polish in this
  phase.

## Consequences

- MVP PDFs are simple text PDFs, not polished resume layouts.
- MVP DOCX files are valid minimal Office Open XML documents without advanced
  styles.
- Future renderer adapters can replace internals without changing document
  provenance contracts.
- Tests should focus on evidence links, unsupported-claim behavior, artifact
  creation, and export metadata.

## Rejected Alternatives

- Add `python-docx` immediately: useful later, but not required for evidence
  contracts.
- Add WeasyPrint immediately: strong PDF option, but native dependency risk is
  premature.
- Use Pandoc as default: powerful but requires an external binary and configured
  PDF engine.
- Generate only Markdown forever: too limiting for planned phase 2 document
  workflows.

## Verification

- Plan 006 tests create Markdown, DOCX, and PDF artifacts from public fixtures.
- Export metadata points back to canonical SQLite records.
- Unsupported claims are blocked or labeled before rendering.
