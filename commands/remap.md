---
description: Self-contained remap of an ICM workspace after any structural change. Detects rooms, departments, work patterns. Regenerates routing tables, validates pointer integrity, syncs `.claude/settings.local.json` skillOverrides per room, checks Convention 17 (room template) and 19 (Pattern A/B declared). Dry-runs first, asks for confirmation, then writes.
---

# /icm:remap

The single command to run after ANY structural change in an ICM workspace.

Walk the workspace, detect departments + rooms + work patterns, regenerate routing tables, validate every pointer resolves, sync `.claude/settings.local.json` `skillOverrides` from each room's declared skills, check Convention 17/19/20 compliance.

## Scope (what it touches)

| Concern | What `/icm:remap` does |
|---|---|
| **Root `AGENTS.md` routing** | Regenerate the routing table from disk reality (departments + top-level rooms). Preserve meta rows. |
| **Department `CONTEXT.md` routing** | If a department's `CONTEXT.md` has a `## Routing` section, regenerate it from the rooms inside that department. |
| **Pointer integrity** | Validate every path mentioned in `Read` / `Inputs` columns / sections resolves. Flag broken pointers. |
| **`.claude/settings.local.json` skillOverrides** | For each room, read its `CONTEXT.md` Skills section, regenerate `skillOverrides` block. Workspace root gets baseline `"off"` for every workspace-discoverable skill. |
| **Convention 17 check** | Every room has `CONTEXT.md` + `docs-<roomname>/` + `.claude/settings.local.json`. Flag rooms missing any of these. |
| **Convention 19 check** | Every department `CONTEXT.md` declares Pattern A or Pattern B explicitly. |
| **Convention 20 check** | Pattern A projects have `_state.json` (no folder-hierarchy lifecycle, no emoji marker files). |
| **Dry-run by default** | Always run dry-run first; show user proposed changes; ask before writing. |

## What you (the agent) do

1. **Locate scripts.** Resolve `$SCRIPTS` in this order:
   - `$CLAUDE_PLUGIN_ROOT/scripts/` if the env var is set.
   - Walk up from this command file until you find a sibling `scripts/icm_remap.py`.
   - Try `~/.claude/plugins/icm/scripts/` and `~/.claude/plugins/cache/**/icm/scripts/`.
   - Otherwise ask the user.

2. **Run dry-run first:**
   ```
   python "$SCRIPTS/icm_remap.py" "$ARGUMENTS"
   ```
   (If `$ARGUMENTS` is empty, use the cwd.)

3. **Show the user the proposed changes:**
   - Routing table diff (root AGENTS.md + each department's CONTEXT.md)
   - `skillOverrides` diff per room
   - Convention violations (17, 19, 20)
   - Broken pointers

4. **Run audit alongside** to surface broken pointers:
   ```
   python "$SCRIPTS/icm_audit.py" "$ARGUMENTS"
   ```

5. **If there are no changes and no violations**, say so plainly. Done.

6. **If there are changes**, ask the user to confirm (AskUserQuestion: write / skip / abort). On confirm:
   ```
   python "$SCRIPTS/icm_remap.py" "$ARGUMENTS" --write
   ```

7. **Report**:
   - If the audit is clean: say only "Maps updated." (one line).
   - If the audit has errors or warnings: surface each issue with path and reason, then list any follow-up actions (e.g. "room X has no CONTEXT.md — run `/icm:set-up` on that folder").

## Department detection

A department is a top-level numbered folder (`0-`, `1-`, `2-`...) that:
- Has its own `CONTEXT.md`
- Contains one or more rooms (numbered sub-folders)
- Optionally has `docs-<deptname>/`

When `/icm:remap` finds a department, it routes through it (root `AGENTS.md` routing table has a row pointing to the department; the department's own `CONTEXT.md` has a sub-routing table for its rooms).

## Pattern A vs Pattern B detection

Inferred from the department's `CONTEXT.md`:
- "Pattern A" or `projects/` folder exists at department top → Pattern A
- "Pattern B" or `workbench-*` exists in rooms → Pattern B
- Neither → Convention 19 violation, flagged

## Invariants

- Never write without user confirmation when there are real changes.
- Always run audit after a write so the user sees the post-state.
- Meta rows (`(here)`, `—`) authored by the user are preserved automatically.
- Never delete a room's existing `skillOverrides` entry without listing it as a removal in the diff.
- Never modify `instrucoes.md`, `prompts/`, or any `docs-<scope>/` content (Layer 3 read-only).

## Args

`$ARGUMENTS` — optional workspace path (defaults to cwd).

## Implementation status

The current Python script (`scripts/icm_remap.py`) implements only the **root routing table regeneration** (Convention 15). The expanded scope above is the **target spec**; the missing pieces are tracked in `PENDING-WORK.md` §3 of the workspace using this plugin. Until full implementation lands, agents invoking `/icm:remap` should manually handle the missing pieces and surface them to the user.

Implementation roadmap (priority order):
1. Detect departments + nested rooms (Convention 19)
2. Regenerate department-level routing tables
3. Generate `skillOverrides` from each room's CONTEXT.md "Skills" section
4. Write workspace root `.claude/settings.local.json` baseline (all skills `"off"`)
5. Check Convention 17 / 19 / 20 compliance and flag violations
6. Add tests covering each new capability
