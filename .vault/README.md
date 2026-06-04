# res2jobWorks .vault

This `.vault/` directory is the repo-local working memory for `res2jobWorks`.
It is operational memory for plans, evidence, decisions, reusable fixes, blockers,
goal runs, and visual explanations.

## Structure

- `PLAN.md` - project roadmap, current state, active plan index, cross-plan risks, and next actions
- `plans/` - executable feature plans for implementation and validation
- `research/` - local code research, previous-session recovery, and external technical research
- `decisions/` - durable architecture, product, data, workflow, and safety decisions
- `solutions/` - reusable implementation patterns discovered during execution
- `encounters/` - failures, blockers, surprises, root causes, and prevention rules
- `goals/` - long-running native `/goal` or multi-plan `$lfg` orchestration overlays
- `visuals/` - self-contained HTML companions for roadmap and architecture diagrams

## Usage Rules

- Keep this vault focused on active engineering work.
- Prefer updating the existing relevant plan or note over creating duplicates.
- Feature plans use `###-feature-topic-YYYY-MM-DD.md`.
- Research notes use descriptive names such as `project-context-YYYY-MM-DD.md`.
- Decisions, solutions, and encounters use concise topic filenames because their directories provide the type.
- Update `PLAN.md` whenever a feature plan is created, completed, paused, or replaced.
- Promote durable choices into `decisions/`.
- Capture reusable implementation patterns in `solutions/`.
- Capture only recurrence-preventing blockers and surprises in `encounters/`.
- Use goal-run folders only when a long-running objective coordinates more than one feature plan.
- Visual companions should be self-contained and safe to open locally in a browser.

## Relationship to Obsidian

Repo-local `.vault/` is the implementation memory for the codebase.
The Obsidian project note at `/home/gilgames/Vault/01_Projects/res2jobworks/res2jobworks.md`
is the strategic, human-facing rollup. Promote only major milestones, project
direction, and durable strategic decisions there.
