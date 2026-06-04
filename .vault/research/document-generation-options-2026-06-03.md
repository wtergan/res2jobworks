---
date: 2026-06-03
status: complete
related_plan: ".vault/plans/006-tailoring-documents-phase2-2026-06-03.md"
---

# Document Generation Options

## Context

Plan 006 expands res2jobWorks from evaluation/tracking into evidence-backed
tailoring, cover letters, application answers, and generated documents. The
rendering stack must stay local-first, inspectable, and testable. Generated
documents remain artifacts derived from SQLite evidence, not canonical state.

## Options Reviewed

### Markdown-first rendering

- Python-Markdown documents a library and CLI for converting Markdown to HTML
  and supports official extensions through explicit configuration.
- Markdown is already an export format in this repo and is easy to inspect in
  tests.
- Risk: Markdown alone is not a final resume format for many application
  portals.

Source: https://python-markdown.github.io/extensions/

### Direct DOCX construction

- `python-docx` provides a Python API for creating and editing Word documents,
  including paragraphs, headings, and lists.
- It is suitable for richer DOCX styling later, but adding it now would expand
  dependencies before the evidence contracts are proven.
- A minimal Office Open XML writer can cover deterministic MVP tests without a
  dependency, then be replaced by `python-docx` behind the same renderer
  contract.

Source: https://python-docx.readthedocs.io/en/latest/user/quickstart.html

### HTML/CSS to PDF

- WeasyPrint turns HTML and CSS into PDF and supports print-oriented layout.
- It is a good future adapter for polished resumes, but it can require native
  rendering dependencies depending on the environment.
- Keep it optional until Markdown/DOCX/PDF artifact contracts are stable.

Source: https://weasyprint.org/?lang=en

### Pandoc conversion

- Pandoc can convert Markdown to HTML, DOCX, and PDF from the command line.
- It is powerful for document workflows, but it introduces a binary dependency
  and PDF output depends on a configured PDF engine.
- Treat it as an optional external adapter, not the default local MVP renderer.

Source: https://pandoc.org/getting-started.html

## Recommendation

Use a staged rendering stack:

1. Markdown is the primary MVP document artifact.
2. Minimal stdlib DOCX and PDF emitters provide deterministic structural
   artifacts for tests and local use.
3. `python-docx`, WeasyPrint, and Pandoc remain optional future adapters behind
   the same renderer interface.

This keeps Plan 006 focused on provenance and review semantics instead of
toolchain setup. The rendering contract should record artifact metadata in
SQLite exports and require every draft or diff to carry source evidence or an
explicit inference label.

## Validation Notes

- Tests should assert document structure and provenance metadata rather than
  pixel-perfect PDF layout.
- Tests should prove unsupported claims are labeled or blocked.
- Absolute/traversing output paths should continue to be rejected by existing
  export path validation.
