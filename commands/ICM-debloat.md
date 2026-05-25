---
description: Audit a folder for bloat (oversized CONTEXTs, dead outputs, duplicates, superseded drafts) and archive flagged items. Dry-run by default, archive (not delete) on confirmation.
---

# /ICM-debloat

Inspect a folder for bloat and propose what to archive. Nothing is deleted; flagged items move to `<workspace-root>/_archive/<timestamp>/` with a manifest.

## What you (the agent) do

1. **Locate scripts.** Resolve `$SCRIPTS` in this order:
   - `$CLAUDE_PLUGIN_ROOT/scripts/` if the env var is set.
   - Walk up from this command file until you find a sibling `scripts/icm_debloat.py`.
   - Try `~/.claude/plugins/icm/scripts/` and `~/.claude/plugins/cache/**/icm/scripts/`.
   - Otherwise ask the user.

2. **Resolve target:**
   - If `$ARGUMENTS` is empty, prompt the user (AskUserQuestion) for the folder to debloat. Offer the workspace root and each top-level workspace / stage folder as options.
   - Otherwise use `$ARGUMENTS`.

3. **Run dry-run:**
   ```
   python "$SCRIPTS/icm_debloat.py" "<target>"
   ```

4. **Summarize the proposals** grouped by category:
   - `abandoned_output` — empty/tiny output files older than 30 days
   - `duplicate_reference` — same filename appearing in multiple `references/` folders
   - `oversized_context` — CONTEXT.md files over the token budget (review only, not archived)
   - `superseded_draft` — `*_draft.md` files where a `*_final.md` exists and the draft is stale

   For each item, show: path, reason, category.

5. **Ask the user to confirm** (AskUserQuestion: apply all / apply some (lets them list which) / abort).

   - For "apply all": run `icm_debloat.py "<target>" --apply`.
   - For "apply some": create a smaller set by removing the unwanted entries — but this is best done by the user re-running the command after manually removing the items they don't want auto-archived. Don't try to cherry-pick across the script boundary.

6. **After --apply runs**, report: how many items archived, archive directory path, manifest path.

7. **For `oversized_context` items**, do not archive. Instead, suggest extracting reference material from the oversized CONTEXT.md into a `references/` file. Offer to do this in a follow-up turn.

## Invariants

- Never delete. Always archive.
- Always dry-run first. Never `--apply` without explicit user confirmation.
- Never archive a stage's CONTEXT.md or AGENTS.md — those are load-bearing.

## Args

`$ARGUMENTS` — optional folder path. If empty, agent prompts the user.
