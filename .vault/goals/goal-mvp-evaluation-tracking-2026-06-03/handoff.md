# Goal Handoff

## Resume Here

- Active goal run: `.vault/goals/goal-mvp-evaluation-tracking-2026-06-03/`
- Current milestone/task: `M6.T1`
- Current branch/worktree: detached worktree at `/home/gilgames/Code/res2jobworks/.worktrees/res2jobworks-phase2-documents`
- Active plan: `.vault/plans/006-tailoring-documents-phase2-2026-06-03.md`
- GitHub repo: `https://github.com/wtergan/res2jobworks`

## Latest Known State

Plans 001, 002, 003, 004, 005, and 006 are complete, committed, and published. The required two-plan refactorer gates after plan 002, plan 004, and plan 006 are complete.

Implemented plan 002 scope:

- Package-contained SQL migration and migration runner for the canonical SQLite workspace.
- Explicit `SQLiteRepository` APIs for profiles, resume sources, jobs, job sources, evaluations, citations, applications, status events, notes, exports, and agent runs.
- Citation ownership validation for evaluation profile/job, application/evaluation job consistency, parent-record validation with `RepositoryError`, bounded status values, append-only status history, export path validation, and recursive secret redaction.
- Public fixture seed helper exported from the root package and verified from an installed wheel.
- SQLite data-layer ADR and reusable repository-pattern solution note.
- Internal privacy helper extraction published as `6fc7803` after the refactorer gate.

Implemented plan 003 scope:

- Modular command handlers for workspace init, profile/job import, deterministic cited evaluation, application add/update/list, and Markdown/CSV tracker exports.
- Registry availability for only implemented command handlers.
- Deterministic-first evaluation ADR and cited-evaluation workflow solution.
- Export documentation that keeps Markdown/CSV as generated artifacts from SQLite.
- Command-envelope failure handling for duplicate deterministic IDs and unsupported rubric IDs.

Implemented plan 004 scope:

- CLI direct commands and `res2jobworks run <command-id> --json --input key=value` registry runner over core command handlers.
- Read-only TUI and static local web dashboard renderers over `jobs.list` and `jobs.show`.
- Full citation-backed `jobs.show` query envelopes for UI detail views.
- Registry-driven wrapper generator for Codex and Hermes plus documented Claude/OpenCode/Gemini stubs.
- Client parity tests proving CLI runner output matches direct core command envelopes.
- Post-review fixes remove unimplemented `filters` from available registry metadata, add wrapper invocation parity, keep the web error path accessible, and correct stale wrapper/plan docs.

Implemented plan 005 scope:

- Automation capture contracts import reviewed job text through `jobs.import` and persist sanitized URL, capture timestamp, review state, and validated relative artifact paths in SQLite `job_sources` records.
- `CapturedJobSource`, `SourceCaptureAdapter`, and `FixtureCaptureAdapter` provide browser-free source capture contracts for fixtures/local fakes.
- `automation.capture_job` and `automation.prepare_fill_review` are available through the shared registry and CLI `res2jobworks run` dispatcher.
- Fill-review planning rejects credential-like field names, requires the human-review state, and returns `submission_allowed: false`.
- TUI and web detail views surface captured evidence URL/readable review state; docs describe the no-submit, no-credentials, no-session boundary.

Implemented plan 006 scope:

- Evidence bundles load profile, resume source, job source, evaluation, and citation records from SQLite before drafting.
- Tailoring suggestions, resume diffs, cover letters, and application-answer drafts carry source evidence and require human review.
- Unsupported requested focus areas are labeled instead of converted into claims.
- Deterministic readiness checks label ATS/readability signals as local deterministic checks.
- Markdown, minimal DOCX, and minimal PDF renderers write generated artifacts and record export metadata without mutating canonical profile/job state.
- Document commands are available through the shared registry and CLI `res2jobworks run` dispatcher.
- Provider metadata matches are not trusted as supported document claims unless verified against stored profile/citation evidence; unverified provider skills are labeled as unsupported inferences.
- Rendering uses a temporary artifact and only finalizes the requested output path after export metadata is recorded, cleaning up the temp file on metadata failure.
- `documents.draft_application_answer` is available through the package command wrapper, CLI runner, and shared command registry.

## Validation Evidence

- `uv run --extra dev pytest -q tests/db` -> `29 passed`
- `uv run --extra dev pytest -q` -> `43 passed`
- `uv run --extra dev ruff check .` -> pass
- `uv build` -> built sdist and wheel
- Fresh wheel install from `/tmp` -> packaged fixtures and migration loaded, valid status insert worked, camelCase access-token/client-secret metadata redacted while token usage counts remained intact, and Windows absolute export paths were rejected
- Source checkout seed from `/tmp` -> sample workspace created without cwd-relative fixture access
- Two-plan refactorer gate -> `29` DB tests, `43` full tests, Ruff, whitespace check, and package build passed
- Plan 003 -> `14` workflow tests, `58` full tests, Ruff, build, diff check, and fresh installed-wheel workflow smoke passed
- Plan 004 -> `10` focused interface/wrapper/parity tests passed
- Plan 004 -> `68` full tests passed
- Plan 004 -> Ruff passed
- Plan 004 -> `uv build` built sdist and wheel
- Plan 004 -> installed-wheel smoke passed for `res2jobworks run`, evaluation citations, and `res2jobworks-generate-wrappers`
- Plan 004 browser MCP -> blocked by missing Chrome; encounter captured
- Plan 004 refactor/review follow-up -> `26` focused tests, `70` full tests, Ruff, and build passed
- Plan 005 initial focused gate -> `16` automation/security/UI/workflow/registry/wrapper tests passed
- Plan 005 security/accessibility hardening -> `20` focused tests passed after URL sanitization, evidence path validation, credential-field rejection, terminal control stripping, and readable review labels
- Plan 005 -> `80` full tests passed
- Plan 005 -> Ruff passed
- Plan 005 -> `uv build` built sdist and wheel
- Plan 005 hardening -> `20` focused tests, `84` full tests, Ruff, build, sanitized URL smoke, and credential-field rejection smoke passed
- Plan 006 -> `8` document tests passed
- Plan 006 -> `93` full tests passed
- Plan 006 -> Ruff passed
- Plan 006 -> `uv build` built sdist and wheel
- Plan 006 -> CLI smoke labeled unsupported `Kubernetes` and rendered a PDF artifact with export metadata
- Plan 006 re-review fixes -> `17` focused tests passed
- Plan 006 re-review fixes -> `96` full tests passed
- Plan 006 re-review fixes -> Ruff passed
- Plan 006 re-review fixes -> `uv build` built sdist and wheel

## Review State

Verifier agents approved the final plan 002 diff after status enums, source fallback, camelCase redaction, and Windows export-path fixes. The follow-up refactorer gate made a small privacy-helper extraction and passed validation.

Plan 003 verifier state:

- validator: `APPROVED`
- reviewer: `APPROVED`
- security: `APPROVED`
- pattern-detector: `APPROVED`

Plan 006 verifier state:

- validator: `APPROVED`
- pattern-detector: `APPROVED`
- security: `APPROVED`
- reviewer: `APPROVED`
- refactorer gate after Plans 005-006: `APPROVED`

- validator: `APPROVED`
- reviewer: `APPROVED`
- security: `APPROVED`
- pattern-detector: `APPROVED`

## Next Action

1. Continue with the next user-selected feature or planning lane.
2. Preserve the no-default-auto-submit, SQLite canonical-state, and public-generic fixture boundaries.

## Stop Conditions

- Do not use private dogfooding resume data, add provider-backed drafting, or add submit behavior before explicit user approval and security review.
