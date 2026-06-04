# Skills Package

Generated agent wrapper support lives here.

The generator reads `commands/registry.yaml` and emits agent-facing wrapper
artifacts that call the shared CLI/API command contract. Wrappers must not embed
product behavior, scoring rules, SQLite writes, or export logic.

Generate source-tree wrappers with:

```bash
python packages/skills/scripts/generate_agent_wrappers.py --output .generated/agent-wrappers
```
