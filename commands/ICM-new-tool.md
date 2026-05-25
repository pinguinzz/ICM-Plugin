---
description: Create a new tool (skill) inside the current ICM workspace and wire it into the routing table. Like /skill-creator but ICM-aware.
---

# /ICM-new-tool

Author a new reusable skill scoped to this workspace, place it in the right folder, and register it on the routing-table row that should use it.

## What you (the agent) do

1. **Locate scripts.** Resolve `$SCRIPTS` in this order:
   - `$CLAUDE_PLUGIN_ROOT/scripts/` if the env var is set.
   - Walk up from this command file until you find a sibling `scripts/icm_register_tool.py`.
   - Try `~/.claude/plugins/icm/scripts/` and `~/.claude/plugins/cache/**/icm/scripts/`.
   - Otherwise ask the user.

2. **Detect workspace:**
   ```
   python "$SCRIPTS/icm_detect.py" .
   ```
   If not an ICM workspace, stop and suggest `/ICM-set-up`.

3. **Gather inputs from the user (AskUserQuestion, batch where possible):**
   - **Name** of the tool (short, kebab-case). Example: `web-search`, `humanizer`, `image-prep`.
   - **One-line description** that will be the trigger sentence (what kind of request should fire this tool?).
   - **Scope**:
      - workspace-global → `skills/<name>/SKILL.md`
      - specific workspace → `<workspace>/skills/<name>/SKILL.md`
      - specific stage → `stages/<stage>/skills/<name>/SKILL.md`
   - **Wire into** which routing-table row? (Show the user the current rows from the workspace's `AGENTS.md` and ask which `Task` substring this tool serves. If "none for now", skip the wire-in.)

4. **Generate the SKILL.md:**
   ```
   python "$SCRIPTS/icm_register_tool.py" \
       --workspace "<scope-folder>" \
       --tool-name "<name>" \
       --tool-description "<one-liner>" \
       --target-folder "skills" \
       [--wire-into "<task substring>"]
   ```

5. **Open the new `SKILL.md`** and fill in the TODO sections by interviewing the user:
   - When to use this skill (the trigger conditions).
   - What the skill does in 1–2 sentences.
   - Inputs the skill expects.
   - Step-by-step process.
   - What it produces (outputs).

6. **Run remap** to refresh the routing table everywhere:
   ```
   python "$SCRIPTS/icm_remap.py" <workspace-root> --write
   ```

7. **Run audit** and report. If audit shows issues with the newly wired row, fix them with the user before declaring done.

## Invariants

- Skill `name` becomes a folder name and a YAML field. Stick to kebab-case, no spaces, no caps.
- Always wire the skill into a Task row that will actually invoke it. An unwired skill is dead weight.
- Description (frontmatter) is what triggers the skill. Make it specific — vague descriptions = misfires.

## Args

`$ARGUMENTS` — optional tool name (skip the first question if provided).
