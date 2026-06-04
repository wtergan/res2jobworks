---
date: 2026-06-04
related_plan: ".vault/plans/002-sqlite-evaluation-tracking-model-2026-06-03.md"
type: solution
---

# SQLite Repository Pattern

## Pattern

- Keep migrations as package resources under
  `res2jobworks_core.db.migrations`.
- Apply migrations before repository construction finishes.
- Use `PRAGMA foreign_keys = ON` for every connection.
- Decode `*_json` columns at repository boundaries so clients receive typed
  dictionaries and lists.
- Validate required fields before SQL execution and raise `RepositoryError`
  rather than silently inserting malformed records.
- Treat application status history as append-only events; only update the
  `applications.current_status` pointer.
- Record exports as generated artifacts pointing back to canonical records.
- Redact known secret-bearing keys before persisting provider metadata, export
  metadata, or agent run input/output payloads.
- Package public seed fixtures beside the core package so sample workspace
  creation works from installed distributions as well as source checkouts.
- Validate seed fixture text before inserting it into canonical SQLite state.
- Reject absolute or parent-traversing export artifact paths at the repository
  boundary.

## Verification

Plan 002 repository tests cover migrations, profile/job source persistence,
required and persisted evaluation citations, append-only status events, export
references, note validation, agent run records, provider/agent redaction,
package fixture seeding, source-checkout fixture seeding, string database paths,
list APIs, and export path validation.
