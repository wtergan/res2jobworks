# Browser Evidence Capture Pattern

## Context

Plan 005 adds browser-assisted job-source capture while preserving SQLite as the canonical product store and keeping automation behind human review.

## Pattern

- Treat browser extraction as a client-side capture step that produces text plus evidence metadata.
- Import captured text through the same `jobs.import` workflow used by manual text/file imports.
- Persist sanitized URL, capture timestamp, review state, and validated relative artifact paths in `job_sources.metadata`.
- Return command envelopes from automation commands so CLI, wrappers, tests, and later browser adapters share the same contract.
- Keep fill support as a review plan with `submission_allowed: false` unless a future explicit non-default path is designed and reviewed.

## Boundaries

- Do not store credentials, cookies, session state, or private fixture data in capture metadata.
- Strip URL fragments, reject userinfo URLs, remove sensitive query parameters, and reject absolute/traversing evidence paths.
- Do not bypass core import, SQLite persistence, or command registry contracts.
- Do not add a default submit command.

## Verification

- `uv run --extra dev pytest -q tests/automation tests/security tests/tui tests/web tests/workflows/test_job_import_should_store_browser_evidence_metadata.py tests/core/test_available_sqlite_commands_should_accept_database_path.py tests/core/test_registry_entries_should_have_required_metadata.py tests/wrappers/test_available_agent_commands_should_match_runner_inputs.py` -> `20 passed`
- `uv run --extra dev pytest -q` -> `84 passed`
- `uv run --extra dev ruff check .` -> pass
- `uv build` -> built sdist and wheel
