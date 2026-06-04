# TUI App

Read-only terminal dashboard renderer over the same core command envelopes used
by the CLI and web dashboard.

This MVP keeps the TUI implementation intentionally small: it renders the job
queue, current tracking status, latest score, and evaluation summaries from
SQLite-backed command handlers. Future interactive TUI work should keep
mutations in core commands.
