---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/005-browser-automation-human-review-2026-06-03.md"
---

# ADR: No Default Auto-Submit

## Context

The prior session, repo instructions, and Obsidian plan all state that browser
automation should support draft, fill, review, and evidence capture with
explicit human control before submission. Default behavior must never
auto-submit job applications.

## Decision

The default product will not auto-submit job applications. Browser automation
may capture job descriptions, prepare drafts, fill forms, preserve evidence, and
surface review states. Any future submission behavior requires an explicit,
separate user-approved scope and must remain outside the default MVP path.

## Drivers

- Job applications are high-stakes user actions.
- Automation can misread forms, terms, identity fields, or required context.
- Public-generic defaults should be safe and trust-building.
- Human review preserves accountability and lets users correct generated drafts.

## Alternatives Considered

| Option | Pros | Cons | Why Not |
|---|---|---|---|
| Fully autonomous applications | Maximum automation | High risk and poor user control | Rejected as default |
| No browser automation | Safest implementation | Misses source capture and workflow assistance | Too limiting for project goals |
| Submit behind a hidden flag | Convenient later | Easy to invoke accidentally and hard to message | Requires explicit future plan and review |

## Consequences

- Plan 005 must include blocked-submission tests.
- UI and CLI wording must clearly distinguish draft/fill/review from submit.
- Credentials, cookies, and session data must not be stored in repo artifacts or
  unsafe logs.

## Verification

- `pytest -q tests/automation tests/security` after plan 005.
- Security review before any real-site automation.
- Manual review of CLI/UI copy for no-submit ambiguity.

## Related Artifacts

- Plan: `.vault/plans/005-browser-automation-human-review-2026-06-03.md`
- Research: `.vault/research/project-context-2026-06-03.md`
