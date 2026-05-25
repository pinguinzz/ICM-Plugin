---
description: Answer methodology questions about ICM — layers, routing, stage contracts, conventions, when-to-use. Grounded in the plugin's docs, not paraphrased.
---

# /icm:help

Answer ICM methodology questions using the plugin's documentation as the source of truth.

## What you (the agent) do

1. **Locate the plugin docs.** Resolve `$DOCS` in this order:
   - `$CLAUDE_PLUGIN_ROOT/docs/` if the env var is set.
   - Walk up from this command file until you find a sibling `docs/` directory containing `LAYERS.md`.
   - Try `~/.claude/plugins/icm/docs/` and `~/.claude/plugins/cache/**/icm/docs/`.
   - Otherwise ask the user.

2. **Load the docs into context:**
   - `docs/LAYERS.md` — the 5-layer hierarchy
   - `docs/CONVENTIONS.md` — the 15 rules
   - `docs/STAGE-CONTRACT.md` — Inputs/Process/Outputs format
   - `docs/ROUTING.md` — how routing tables work

3. **Answer the user's question** (`$ARGUMENTS`) using ONLY what's in those files. If the answer isn't in the docs, say so plainly — don't paraphrase from your training data, which may drift from the methodology.

4. **Cite the source.** End each answer with the doc + section it came from. Example: "—from `docs/LAYERS.md`, §Reading order."

5. **If the user is asking about how to DO something** (set up, debloat, add a tool), redirect them to the appropriate `/icm:*` command rather than walking them through it manually.

## Args

`$ARGUMENTS` — the user's methodology question. If empty, ask them what they want to know.

## Common questions and where to find the answer

| Question | Doc |
|---|---|
| "What are the 5 layers?" | `LAYERS.md` |
| "What is a stage contract?" | `STAGE-CONTRACT.md` |
| "What's the difference between Layer 3 and Layer 4?" | `LAYERS.md` § factory vs product |
| "How do routing tables work?" | `ROUTING.md` |
| "What are the rules I have to follow?" | `CONVENTIONS.md` |
| "When should I split a stage?" | `CONVENTIONS.md` § One stage, one job |
| "Why is my CLAUDE.md a one-liner?" | `CONVENTIONS.md` § Compatibility stubs |
