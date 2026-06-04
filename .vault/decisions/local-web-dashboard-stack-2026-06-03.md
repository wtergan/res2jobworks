# Local Web Dashboard Stack

Date: 2026-06-03
Status: Accepted

## Decision

Use a static Python HTML renderer over core command envelopes for the MVP 1
local web dashboard.

## Context

Plan 004 needs a browser-readable dashboard, but the product truth already lives
in SQLite-backed core commands. Introducing a web framework before mutation and
routing needs are clear would add packaging and runtime surface without making
the MVP evaluation tracker more reliable.

## Consequences

- The dashboard can be served by any local HTTP wrapper or opened as generated
  HTML.
- Tests can verify the semantic HTML and command-backed data without a dev
  server.
- Future FastAPI, Vite, or server-action work must keep the same command
  envelope boundary instead of moving product logic into the web layer.
- Live browser verification still depends on a host browser being available.
