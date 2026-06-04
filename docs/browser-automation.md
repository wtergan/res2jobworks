# Browser Automation

res2jobWorks browser automation is assistive by default. It can capture job
source text, preserve evidence, and prepare draft fill instructions, but it does
not submit job applications.

## Default Safety Boundary

Allowed by default:

- Capture visible job-description text from a user-provided local page or URL.
- Preserve source URL, captured text, timestamp, and optional local artifact
  paths as evidence.
- Import captured job text through the same core workflow as manual text/file
  imports.
- Prepare draft application fields and fill instructions for human review.

Not allowed by default:

- Submit applications.
- Store credentials, cookies, session tokens, browser profiles, authorization
  headers, or raw credential fields.
- Bypass paywalls, CAPTCHAs, explicit user review, or site terms.
- Treat browser automation as the only import path.

## Evidence

SQLite remains canonical. Browser capture evidence is stored as source metadata
attached to imported job records. Screenshots or exported files are local
artifacts referenced from SQLite metadata; they are not the source of truth.

## Review States

Draft/fill support must clearly indicate whether a user still needs to review a
field. The default product path stops before submission even if every field has
been drafted.
