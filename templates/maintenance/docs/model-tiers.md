# Model tiers — maintenance rooms (editable)

> The model each maintenance room runs on, and what it must read before acting. **Edit this table to
> re-tune cost vs capability — no code change needed.** `dispatch-subagent` reads the tier from here when
> entering a room; each room's `CONTEXT.md` points here instead of hardcoding a model.

| Room | Tier | Model | Reads before acting | Entry |
|------|------|-------|---------------------|-------|
| `modify-room` | cheap | haiku | condensed "how to evolve a room" rules + the target room only | in-context, or cheap subagent |
| `janitor` | cheap–mid | haiku / sonnet | the janitor procedure + the target files (mostly mechanical) | subagent |
| `audit` | mid | sonnet | full canon + its own `docs/memory/` | subagent, clean context |
| `modify-workspace` | mid–high | sonnet / opus | **full** canon (all maintenance `docs/`) | **fresh** subagent, clean context, after CR / human approval |

Model ids: haiku `claude-haiku-4-5-20251001` · sonnet `claude-sonnet-4-6` · opus `claude-opus-4-8`.

## How it's used
1. A maintenance op is requested → caller resolves the target room's tier from this table.
2. It invokes `dispatch-subagent` (worker mode) with `model` = the tier's model.
3. The room's `CONTEXT.md` Inputs name *condensed* (cheap) or *full* (heavy) docs to read — matching the tier.
4. To change a room's cost/capability, edit the `Tier`/`Model` cell here. Nothing else changes.
