---
description: Create new ICM structure — a workspace, department, room, or sub-room. Backbone-locked relentless intake, then scaffold into the fixed 5-layer skeleton from the plugin's templates. Additive only; never mutates existing structure.
---

# /icm:new

Author new ICM structure at any granularity. The skeleton is **fixed** — you fill it and adapt to what is asked, you never reinvent
it. Intake is **relentless** but keep it **backbone-locked**: ask everything needed for the contracts, lock the skeleton,
don't invent new conventions.

`/icm:new` is the front-door to the **`modify-workspace`** maintenance room. If a workspace already exists,
**route through its `maintenance/modify-workspace/` first** — read that room's `docs/` + memory + any open
CRs + `model-tiers.md`, then act (it's a heavy, gated op). **Greenfield exception:** an empty target has no
maintenance dept yet, so this command *bootstraps* it (step 6 below creates `maintenance/`). Everyday
productive agents never run this — only maintenance ops do.

## What you (the agent) do

1. **Locate the plugin.** Resolve `$ROOT` (the plugin dir, holding `templates/` + `docs/` + `scripts/`):
   a. `$CLAUDE_PLUGIN_ROOT` if set.
   b. Walk up from this command file until you find `templates/parts/` + `.claude-plugin/plugin.json`.
   c. `~/.claude/plugins/icm/`, then `~/.claude/plugins/cache/**/icm/`.
   d. Else ask the user. Don't guess.
   
2. **Read the canon** before authoring: `$ROOT/docs/CONVENTIONS.md` (Invariants/Guidelines) +
   `$ROOT/docs/ROOM-CONTRACT.md` (the contract shape) + `$ROOT/docs/LAYERS.md`.


3. **Guard against mutation.** If creating this node would rename/move/alter anything that already exists,
   STOP and tell the user — `/icm:new` is **additive only**. Adding folders into an
   existing tree structure is fine; Modifying how the folders interact with each other is not.

4. **Determine the scope** (from `$ARGUMENTS` or AskUserQuestion) relentlessly ask about:
   **workspace** · **department** · **room** · **sub-room**. Determine the pipelines needed to achieve the user goal.
   Advise to not build more than one department per session keep it focused on one, then in a new session do another.

5. **Relentless intake (backbone-locked).** Ask only what the contract needs, one focused batch:
   - *workspace:* project name, one-line identity, the departments/rooms it needs, CR-inbox path, naming.
   - *department:* purpose, **work pattern** (sequential vs parallel — it must declare one), its rooms.
   - *room/sub-room:* what it transforms; **Inputs** (name the *section/scope*, not just the file);
     Process steps; Outputs; Done-when; Boundaries (the never-empty "NEVER modify"); whether it needs
     sub-rooms (recursion **by need** only) + a `NN.0` room for human/auto review, when and how many checkpoints.
     Tooling (skills. plugins, MCP servers); decide on what tools or what type of tools are needed to complete the tasks.
   Lock each answer before moving on. Don't fabricate Inputs or steps the user didn't give. Follow the pipeline steps.

6. **Scaffold from templates** into the fixed skeleton:
   - workspace → `root-AGENTS.md` + `workspace-CONTEXT.md` + `stubs/*`, **plus the maintenance dept**:
     copy `$ROOT/templates/maintenance/` to `<workspace>/maintenance/`, vendor the four canon docs as the C5
     fallback into `maintenance/docs/` with lowercase names — `$ROOT/docs/CONVENTIONS.md`→`conventions.md`,
     `LAYERS.md`→`architecture.md`, `ROOM-CONTRACT.md`→`room-contract.md`, `ROUTING.md`→`routing.md` — and copy
     `$ROOT/scripts/icm_check.py`→`<workspace>/scripts/`. (State/markers are covered in `conventions.md`
     Invariant 5; there is no separate state-model doc.) This is the maintenance-first fallback (Q2): the
     skill is the source of truth; the vendored copy is read only when the skill isn't loaded.
   - department → `dept-CONTEXT.md` + its `docs/`.
   - room/sub-room → `room-CONTEXT.md` + `docs/` + a `tools.json` (the canonical tooling model — entries with
     `toolname`/`tool-path`/`when-to-use`/`how-to-use`, paths relative to workspace root; tools live in the
     central `.claude/` store, NOT vendored per room) (+ `NN.0` review sub-room if it earns one).
   Substitute every `{{PLACEHOLDER}}`. Zero-pad numbers. `docs/` (never `docs-<name>/`). No emoji.

7. **Gated-pipeline pattern** (when scaffolding a pipeline department — teach + apply alongside the human, do not hand-wave):
   - **Sub-stages and stages** determine their gates, where to call for a auto-review, when to call a human
   - **Granular rejection:** Goal is to try to make so a rejection refine only the
     rejected sub-piece (+ its descendants), not a whole stage. Auto-review redo within the same `v<N>`; bump `v<N+1>` only if the stage's human gate
     rejects.
   - **Configurable gates** in the workspace `config` (`human` now → `auto` once trained and trusted). Loosen the
     middle stages first; keep humans heaviest at direction (first stages) + final stages.
   - **Think-vs-execute:** the writing room says WHAT (a brief); the production room decides HOW. Separate each step, validate
     each end.
   - **Plan-before-spending** for expensive steps: present an estimated plan; human approves before spend.
   - **Tier by expected value:** pick model/tooling from the run's value tier.
   - **Auto-review** via the `dispatch-subagent` skill (reviewer mode) before the human gate.

8. **Check + report.** Run `python "$ROOT/scripts/icm_check.py" "<workspace-root>"`. If clean: say what was
   created and the next thing to fill. If it flags issues, surface them and fix with the user.

## Invariants

- Never overwrite a non-empty `AGENTS.md` or `CONTEXT.md` without explicit confirmation.
- Additive only. Anything that touches existing structure is human gated.
- Always end with `icm_check.py`. Surface any errors before declaring done.

## Args

`$ARGUMENTS` — optional `<scope> [path]` (e.g. `room dept-content/04-package`). Skips most of the scope questions, focus on that path.
