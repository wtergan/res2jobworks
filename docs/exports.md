# Generated Exports

res2jobWorks treats SQLite as canonical state. Markdown and CSV files are
generated artifacts for review, sharing, or spreadsheet workflows; editing an
export file never mutates the database.

## MVP 1 Tracker Exports

`applications.export` reads stored applications, jobs, and evaluations from the
SQLite repository, writes a relative output path, and records an export row with
the generated path and safe metadata.

Supported formats:

- `markdown` for a human-readable tracker summary.
- `csv` for tabular application pipeline rows.

Absolute paths and parent-directory traversal are rejected so export records stay
portable with the local workspace.
