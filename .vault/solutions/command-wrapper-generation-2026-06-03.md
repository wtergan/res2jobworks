---
date: 2026-06-03
status: accepted
related_plan: ".vault/plans/004-interfaces-and-agent-wrappers-2026-06-03.md"
---

# Command Wrapper Generation Pattern

## Context

Plan 004 needs agent wrappers without creating separate product logic for each
agent. `commands/registry.yaml` already records command IDs, inputs, outputs,
availability, and client targets.

## Pattern

Generate agent wrapper artifacts from the command registry and make each wrapper
call the shared command contract:

```bash
res2jobworks run <command-id> --json --input key=value
```

Codex and Hermes wrappers can be concrete Markdown artifacts now. Agent formats
that are still unstable should receive documented stubs that preserve the same
registry-derived command catalog and invocation contract.

## Guardrails

- Filter wrapper catalogs to commands that list `agent` as a client.
- Preserve registry status so planned commands are visible but not treated as
  callable.
- Return the command envelope emitted by the shared runner without reshaping.
- Do not import core workflow modules or write SQLite from wrappers.
- Keep generated artifacts reproducible and record `manifest.json` with command
  IDs and output files.

## Verification

- `tests/wrappers/test_generated_codex_wrapper_should_call_registry_command.py`
- `tests/wrappers/test_generated_hermes_wrapper_should_call_registry_command.py`
- `tests/wrappers/test_custom_registry_should_drive_generated_wrapper_commands.py`
- `tests/wrappers/test_unstable_agent_formats_should_generate_documented_stubs.py`
