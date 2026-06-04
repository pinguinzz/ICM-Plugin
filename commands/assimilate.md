---
description: Convert an existing folder into an ICM workspace, OR integrity-check an existing ICM workspace. Read-only and plan-mode — it relentlessly grills the structure, reports findings, and emits a plan for later execution. It never mutates anything.
---

# /icm:assimilate

Two paths, one rule: **read-only**. `/icm:assimilate` inspects, grills, and writes a **plan**. It does not
move, rename, delete, or edit a single file. Execution is a separate, human-gated step.

## What you (the agent) do

1. **Locate the plugin.** Resolve `$ROOT` (holds `scripts/icm_check.py` + `docs/`): `$CLAUDE_PLUGIN_ROOT`
   → walk up for `.claude-plugin/plugin.json` → `~/.claude/plugins/(cache/**/)icm/` → else ask.

2. **Determine the path** (`$ARGUMENTS` or cwd) and **detect ICM**: is there an `AGENTS.md` at the root,
   plus the layer signature (numbered rooms / per-folder `CONTEXT.md` / `docs/`)? Branch:

3. **Read the canon** before authoring: `$ROOT/docs/CONVENTIONS.md` (Invariants/Guidelines) +
   `$ROOT/docs/ROOM-CONTRACT.md` (the contract shape) + `$ROOT/docs/LAYERS.md`.

4. Study the structure being assimilated, 

### Path A — already ICM → integrity-check

3a. Run `python "$ROOT/scripts/icm_check.py" "<root>" --json` and read it.
4a. **Relentlessly grill the structure** (the script is mechanical; you do the judgment):
   - **Layer 3/4 classification** — confirm `docs/` (L3) and product folders (`projects/`, `workbench-*`,
     `output/…`) are NOT mistaken for rooms/workspaces. Don't flag them as "missing CONTEXT".
   - **Routing completeness** — descend the numbered dept/room tree; is every real room reachable from a
     routing table? Never propose shrinking a curated table; flag missing rows, don't drop existing ones.
   - **Stale pointers** — scan `AGENTS.md`/`CONTEXT.md` prose for path-like references that don't resolve
     on disk.
   - **One-way refs / canonical home** — flag bidirectional reference links and duplicated authoritative rules.
   - **Oversize** — CONTEXT > 80 / reference > 200 lines (advisory).
5a. **Report the 4 points:** (1) invariant violations (0 expected on a healthy tree); (2) Layer-3/4
   classified correctly; (3) routing not regressed; (4) known wrinkles surfaced as **advisories**, not errors.
6a. **Emit a plan** (`assimilate-plan.md` in the workspace, or print it) listing each finding + a proposed
   fix, ordered, for the human to execute later. **Make no changes.**

### Path B — not yet ICM → conversion plan

3b. Walk the existing tree (Glob/LS). Build a one-page summary of what's there.
Then read enough to understand what it is, what it does, how it could become an ICM work space

4b. **Relentlessly rill toward a 5-layer mapping** — propose which existing folders become L0/L1/L2/L3/L4, and surface
   the common assimilation snags (don't act on them, plan them):
   - `AGENTS.md` that just redirects to another spec file → plan to merge it into the spec.
   - code repo / `package.json` at root, an external data store (Drive/NAS junction), multi-tool config
     pollution (`.cursor/`, `.codex/`…), `agents/<role>/` folders that map to rooms.
   - stale path references in any existing `CONTEXT.md`.
   - Or anything else that could conflict with the ICM.


5b. **Emit a conversion plan** (`assimilate-plan.md`): the proposed layer mapping + the ordered steps to
   reach it (scaffold `AGENTS.md`/stubs, author room contracts, declare work patterns, wire routing).
   Reference the plugin's templates. **Do not create or move any file.**

6b. Ask to call for a `/icm:new` to start assimilating all the learnings and knoledge grilled in the plan. Create a new structure from scratch. Do not modify anything in the original folder, create a new one and copy everything to it.

## Invariants

- **Read-only. Always.** No `mkdir`/`mv`/`rm`/edit. The deliverable is a plan, never a mutation.
- On an already-ICM tree, never restructure — grill + report + plan only.
- Always run `icm_check.py` on Path A and fold its output into the report.

## Args

`$ARGUMENTS` — optional target folder (defaults to cwd).
