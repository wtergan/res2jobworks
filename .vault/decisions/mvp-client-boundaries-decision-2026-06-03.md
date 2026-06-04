---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md"
---

# ADR: MVP Client Boundaries

## Context

The project requires CLI, TUI, web dashboard, browser automation, and agent
wrappers while preserving one product truth. The predecessor `Res2JobFit` already
explored registry-driven agent wrappers, and the new project instructions lock
core ownership of product truth.

## Decision

Keep all clients thin over shared core command/service contracts. The command
registry owns command metadata. Generated wrappers call CLI/API command
contracts and return the stable command envelope. TUI, web, automation, and
agent wrapper code must not duplicate domain logic or mutate state outside core
workflows.

## Drivers

- Equivalent behavior across CLI, TUI, web, and agents.
- Avoid duplicated product logic and drift.
- Keep UI and automation replaceable without changing product truth.
- Make wrappers safe to generate and review.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|---|---|---|---|
| UI owns workflow logic | Faster for one interface | Drifts from CLI/agent workflows | Violates core-owned truth |
| Agent wrappers include prompt logic and product rules | Feels native per agent | Hard to test and keep in sync | Wrappers should call commands |
| Separate APIs per client | Flexible | Multiplies contracts | Shared envelope is simpler |

## Consequences

- Plan 001 must define the stable JSON envelope early.
- Plan 004 must add parity tests.
- Browser automation in plan 005 must feed core import/tracking workflows rather
  than writing separate state.

## Verification

- Registry validation tests in plan 001.
- CLI/wrapper parity tests in plan 004.
- Browser automation tests in plan 005 prove captured sources enter core import
  paths.

## Related Artifacts

- Plan: `.vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md`
- Research: `.vault/research/predecessor-res2jobfit-and-career-ops-2026-06-03.md`
