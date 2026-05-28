# room Contract — Inputs / Process / Outputs

Every room `CONTEXT.md` declares three things. This is the contract. The agent reads it and knows exactly what to load, what to produce, and where to put the result.

## The shape

```markdown
# room 01 — Research

## Purpose
One sentence: what this room transforms.

## Inputs
|From|File/Folder|What to load|
|---|---|---|
|user prompt|—|the topic|
|.folder/|shared/voice.md|style + tone|
|../00-brief/output/|brief.md|scope and constraints|

## Process
1. Step 1 (action verb).
2. Step 2.
3. Step 3.

## Outputs
|To|File|Format|
|---|---|---|
|./output/|research.md|markdown, sections: Key Points, Sources, Open Questions|
|./output/|sources.json|array of {title, url, claim}|

## Done when
- Bullet 1
- Bullet 2

## Hand-off
Next room reads from `./output/`. See `../02-script/CONTEXT.md`.
```

## Why three sections

- **Inputs** make context-loading explicit. The agent doesn't guess what to read.
- **Process** is a recipe a human can follow without the agent. If you can't write it as steps, the room is doing too much.
- **Outputs** define the artifact. The next room's input.

## "Done when"

A short, unambiguous list. Lets the human reviewer (and the agent) know when the room is finished. No "done when it feels right" — be concrete.

## What NOT to put in a room CONTEXT.md

- The voice guide (lives in `shared/voice.md`, referenced in Inputs)
- The brand identity (lives in `_config/brand.md`, referenced in Inputs)
- Personality instructions for the agent ("be creative") — the agent inherits identity from root `AGENTS.md`

Keep room contracts under 500 tokens. If yours is bigger, you're inlining reference material — extract it to Layer 3.
