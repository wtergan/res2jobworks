# Documents Package

Evidence-backed phase 2 tailoring and document generation lives here.

The package reads canonical SQLite records through core repository contracts and
produces reviewable artifacts. Generated documents never become product truth:
they are recorded in the `exports` table with provenance metadata.

Current capabilities:

- evidence bundles from profile, resume source, job source, and evaluation data
- cited tailoring suggestions and reversible section-level resume diffs
- cover letter and application-answer drafts with unsupported inferences labeled
- deterministic ATS/readability readiness checks
- local Markdown, minimal DOCX, and minimal PDF renderers
