---
description: Create new ICM structure — a workspace, department, room, or sub-room. Backbone-locked relentless intake, then scaffold into the fixed 5-layer skeleton from the plugin's templates. Additive only; never mutates existing structure (that needs a CR).
---

# /icm:new

Author new ICM structure at any granularity. The skeleton is **fixed** — you fill it, you never reinvent
it. Intake is **relentless and backbone-locked**: ask the minimum to fill the contract, lock the skeleton,
don't invent.

## What you (the agent) do

1. **Locate the plugin.** Resolve `$ROOT` (the plugin dir, holding `templates/` + `docs/` + `scripts/`):
   a. `$CLAUDE_PLUGIN_ROOT` if set.
   b. Walk up from this command file until you find `templates/parts/` + `.claude-plugin/plugin.json`.
   c. `~/.claude/plugins/icm/`, then `~/.claude/plugins/cache/**/icm/`.
   d. Else ask the user. Don't guess.

2. **Determine the scope** (from `$ARGUMENTS` or one AskUserQuestion):
   **workspace** · **department** · **room** · **sub-room**. For room/sub-room, also get the parent path.

3. **Read the canon** before authoring: `$ROOT/docs/CONVENTIONS.md` (Invariants/Guidelines) +
   `$ROOT/docs/ROOM-CONTRACT.md` (the contract shape) + `$ROOT/docs/LAYERS.md`.

4. **Guard against mutation.** If creating this node would rename/move/alter anything that already exists,
   STOP and tell the user to file a CR — `/icm:new` is **additive only**. Adding a brand-new folder into an
   existing tree is fine; work in a `workbench-<target>/` and let the human promote it.

5. **Relentless intake (backbone-locked).** Ask only what the contract needs, one focused batch:
   - *workspace:* project name, one-line identity, the departments/rooms it needs, CR-inbox path, naming.
   - *department:* purpose, **work pattern** (sequential vs parallel — it must declare one), its rooms.
   - *room/sub-room:* what it transforms; **Inputs** (name the *section/scope*, not just the file);
     Process steps; Outputs; Done-when; Boundaries (the never-empty "NUNCA modifica"); whether it needs
     sub-rooms (recursion **by need** only) + a `NN.0` auto-review.
   Lock each answer before moving on. Don't fabricate Inputs or steps the user didn't give.

6. **Scaffold from templates** into the fixed skeleton:
   - workspace → `root-AGENTS.md` + `workspace-CONTEXT.md` + `stubs/*`.
   - department → `dept-CONTEXT.md` + its `docs/`.
   - room/sub-room → `room-CONTEXT.md` + `docs/` (+ `tools.json` if it declares skills; vendor with the
     workspace's skills-sync) (+ `NN.0-revisao/` if it earns one).
   Substitute every `{{PLACEHOLDER}}`. Zero-pad numbers. `docs/` (never `docs-<name>/`). No emoji.

7. **Gated-pipeline pattern** (when scaffolding a pipeline department — teach + apply, don't hand-wave):
   - **Sub-stages** that each merit their own gate (`NN.1 → NN.2 → NN.3`), so a rejection refines only the
     rejected sub-piece (+ its descendants), not the whole stage.
   - **Granular rejection:** redo within the same `v<N>`; bump `v<N+1>` only if the stage's *final* gate
     rejects.
   - **Configurable gates** in the workspace `config` (`human` now → `auto` once trusted). Loosen the
     middle first; keep humans heaviest at direction (first stage) + final.
   - **Think-vs-execute:** the writing room says WHAT (a brief); the production room decides HOW. Validate
     each end.
   - **Plan-before-generate** for expensive steps: present an estimated plan; human approves before spend.
   - **Tier by expected value:** pick model/tooling from the run's value tier.
   - **Auto-review** via the `dispatch-subagent` skill (reviewer mode) before the human gate.

8. **Check + report.** Run `python "$ROOT/scripts/icm_check.py" "<workspace-root>"`. If clean: say what was
   created and the next thing to fill. If it flags issues, surface them and fix with the user.

## Invariants

- Never overwrite a non-empty `AGENTS.md` without explicit confirmation.
- Additive only. Anything that touches existing structure → CR, not `/icm:new`.
- Always end with `icm_check.py`. Surface any errors before declaring done.

## Args

`$ARGUMENTS` — optional `<scope> [path]` (e.g. `room dept-content/04-package`). Skips the scope question.
