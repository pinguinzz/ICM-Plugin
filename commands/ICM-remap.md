---
description: Regenerate routing tables and validate pointer integrity for an ICM workspace. Dry-runs first, asks for confirmation, then writes.
---

# /ICM-remap

Walk the workspace, find all stages and named workspaces, regenerate the routing table in root `AGENTS.md`, validate that every pointer resolves.

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

3. **Show the user the proposed routing table** (from the script's `routing_table` field). Highlight any difference vs the existing one:
   - New rows (folders added)
   - Dropped rows (folders that no longer exist)
   - Preserved meta rows (those with `Go to = (here)` etc.)

4. **Run audit alongside** to surface any new broken pointers:
   ```
   python "$SCRIPTS/icm_audit.py" "$ARGUMENTS"
   ```

5. **If there are no changes**, say so plainly. Done.

6. **If there are changes**, ask the user to confirm (AskUserQuestion: write / skip / abort). On confirm:
   ```
   python "$SCRIPTS/icm_remap.py" "$ARGUMENTS" --write
   ```

7. **Report**: rows changed, audit summary (errors / warnings), and any follow-up actions (e.g. "stage X has no CONTEXT.md — run `/ICM-set-up` on that folder").

## Invariants

- Never write without user confirmation when there are real changes.
- Always run audit after a write so the user sees the post-state, not just the proposed state.
- Meta rows (`(here)`, `—`) authored by the user are preserved automatically by the script. Don't try to recreate them yourself.

## Args

`$ARGUMENTS` — optional workspace path (defaults to cwd).
