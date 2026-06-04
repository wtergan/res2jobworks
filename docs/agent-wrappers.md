# Agent Wrappers

res2jobWorks agent wrappers are generated from `commands/registry.yaml`.
The registry owns command IDs, descriptions, inputs, outputs, client targets,
and availability status.

## Generate Wrappers

From a source checkout:

```bash
python packages/skills/scripts/generate_agent_wrappers.py --output .generated/agent-wrappers
```

Generate one agent target:

```bash
python packages/skills/scripts/generate_agent_wrappers.py \
  --target-agent codex \
  --output .generated/agent-wrappers
```

Generated paths:

- `codex/SKILL.md`
- `hermes/res2jobworks.md`
- `claude/README.md`
- `opencode/README.md`
- `gemini/README.md`
- `manifest.json`

## Runtime Contract

Wrappers must call the shared CLI/API command contract:

```bash
res2jobworks run <command-id> --json --input key=value
```

They must return the JSON command envelope emitted by that runner. They must not
import core workflow modules, write SQLite directly, implement scoring, or
generate tracker exports themselves.

The current wrapper slice generates contract-ready artifacts. The concrete CLI
or API runner for `res2jobworks run` is a separate plan 004 integration slice.

## Agent Targets

Codex and Hermes receive first-class Markdown wrappers with command catalogs and
contract instructions.

Claude, OpenCode, and Gemini receive documented stubs because native wrapper
formats can shift. The stubs still list registry-derived command contracts so
future native adapters can be filled in without inventing new product behavior.

## Availability

Commands with `status: available` are listed as callable contracts. Commands
with planned status are generated for parity and future adapter work, but should
not be called until the registry marks them available.
