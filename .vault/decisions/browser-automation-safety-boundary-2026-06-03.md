---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/005-browser-automation-human-review-2026-06-03.md"
---

# ADR: Browser Automation Safety Boundary

## Context

Plan 005 adds browser-assisted capture and draft/fill/review workflows after the
manual import, evaluation, tracking, CLI, TUI, web, and wrapper foundations are
already in place. The project guardrails require browser automation to remain a
client over core contracts and explicitly forbid default auto-submit behavior.

## Decision

Browser automation may capture job-source text, preserve source evidence,
prepare drafts, and describe fill actions for human review. It must stop before
submission by default. The default command surface must not include a submit
operation, hidden submit flag, or success-shaped fallback that implies an
application was submitted.

Automation outputs must flow into existing core command envelopes and SQLite
records. Captured evidence belongs in canonical SQLite source records, with
Markdown, CSV, screenshots, and local files treated as artifacts only.

## Allowed By Default

- Extract visible job-source text from user-provided local pages or URLs.
- Capture source URL, capture timestamp, normalized text, and optional local
  artifact references.
- Import captured text through the same job import workflow used by manual text
  and file imports.
- Prepare application field drafts and fill instructions that require explicit
  human review.
- Record blocked submission attempts or review-required states for audit.

## Disallowed By Default

- Submitting applications.
- Storing credentials, cookies, session tokens, authorization headers, or
  browser profiles in repo files, SQLite metadata, logs, exports, or artifacts.
- Bypassing paywalls, CAPTCHAs, terms, permission prompts, or user review.
- Treating browser extraction as the only import path.
- Generating resumes, cover letters, or document answers in MVP 1.

## Verification

- Tests must prove captured job text imports through core workflow commands.
- Tests must prove evidence metadata persists in SQLite source records.
- Tests must prove default automation cannot submit and fill drafts require a
  human-review state.
- Security review must check credential/session logging before any real-site
  automation is considered.

## Related Artifacts

- Plan: `.vault/plans/005-browser-automation-human-review-2026-06-03.md`
- Decision: `.vault/decisions/mvp-no-autosubmit-default-decision-2026-06-03.md`
- Decision: `.vault/decisions/foundational-architecture-2026-06-03.md`
