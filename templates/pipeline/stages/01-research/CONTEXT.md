# Stage 01 — Research

## Purpose

Transform a topic into structured research: key points, sources, narrative angles, open questions.

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| user prompt | — | the topic + any specific framing |
| `../../shared/audience.md` | full file | who we are writing for |
| `references/research-checklist.md` | full file | what "research done" looks like |

## Process

1. Restate the topic in one sentence.
2. List 5–7 key points the audience should walk away with.
3. For each key point, find at least one concrete example or source.
4. List the strongest counter-arguments or open questions.
5. Suggest 2–3 narrative angles (the "way in" to the topic).
6. Write everything to `output/YYYY-MM-DD_<topic-slug>.md`.

## Outputs

| To | File | Format |
|----|------|--------|
| `./output/` | `YYYY-MM-DD_<topic-slug>.md` | markdown — sections: One-Liner, Key Points, Examples, Counter-arguments, Narrative Angles |

## Done when

- Five or more key points, each with one example.
- At least two narrative angles offered.
- At least one honest "I don't know yet" in the open questions.
- File saved under correct name in `output/`.

## Hand-off

Next stage reads from `output/`. See `../02-script/CONTEXT.md`.
