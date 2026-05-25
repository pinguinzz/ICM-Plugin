# Stage 02 — Script

## Purpose

Turn structured research into a finished script that reads aloud cleanly in the project's voice.

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| `../01-research/output/` | most recent research file | the topic, key points, angles |
| `../../shared/voice.md` | full file | tone, rhythm, forbidden openers |
| `../../shared/audience.md` | full file | who you're writing for |
| `references/script-structure.md` | full file | the structure template |

## Process

1. Pick the strongest narrative angle from the research.
2. Draft an opening that is concrete and earns the next 10 seconds.
3. Fill in the structure template (`script-structure.md`).
4. Read it aloud. Cut anything that makes you stumble.
5. Save as `output/<topic>_draft.md`. Iterate to `_v2`, `_final`.

## Outputs

| To | File | Format |
|----|------|--------|
| `./output/` | `<topic>_draft.md` → `<topic>_v2.md` → `<topic>_final.md` | markdown with section headers per scene |

## Done when

- Opens with something concrete (not a rhetorical question).
- Every claim has a concrete example within two sentences.
- Reads cleanly aloud (no stumbles).
- Has a clear ending (not "thanks for watching").

## Hand-off

Production stage reads `<topic>_final.md` from `./output/`. See `../03-production/CONTEXT.md`.
