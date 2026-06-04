# Browser Verification Blocked By Missing Chrome

Date: 2026-06-04
Status: Captured

## Encounter

Plan 004 web verification attempted to use the Playwright MCP browser against a
fixture-rendered dashboard HTML file. The MCP server reported that Chrome was
not installed at `/opt/google/chrome/chrome`.

## Evidence

- `mcp__playwright.browser_resize` failed with `Chromium distribution 'chrome'
  is not found at /opt/google/chrome/chrome`.
- `npx playwright install chrome` required sudo and failed because this session
  cannot provide an interactive sudo password.
- `command -v chromium`, `chromium-browser`, `google-chrome`,
  `google-chrome-stable`, and `chrome` returned no browser binary.

## Resolution

Static web verification proceeded through tests that assert semantic HTML,
responsive CSS hooks, job table data, status, scores, and citation-backed
evidence. Live browser and accessibility-tree verification should be rerun after
Chrome or Chromium is installed on the host.
