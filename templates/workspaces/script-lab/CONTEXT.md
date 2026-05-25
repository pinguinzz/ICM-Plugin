# Script Lab

## Purpose

Where ideas become finished scripts. Three states: idea, draft, final.

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| user prompt | — | topic, angle, constraints |
| `../shared/voice.md` | full file | tone |
| `../shared/audience.md` | full file | who reads/watches |

## Process

1. Capture rough idea in `ideas/<topic>.md`.
2. Develop into a draft in `drafts/<topic>_draft.md`.
3. Iterate to `drafts/<topic>_v2.md`, `_v3.md` as needed.
4. Promote to `final/<topic>_final.md` when ready for production.

## Outputs

| To | File | Format |
|----|------|--------|
| `./ideas/` | `<topic>.md` | rough markdown |
| `./drafts/` | `<topic>_draft.md`, `<topic>_v2.md`, ... | markdown with scene headers |
| `./final/` | `<topic>_final.md` | clean markdown, ready for production |

## Done when

- Opens with something concrete.
- Every claim has a concrete example.
- Reads cleanly aloud.
- Lives in `final/`.

## Hand-off

Production reads from `./final/`. See `../production/CONTEXT.md`.
