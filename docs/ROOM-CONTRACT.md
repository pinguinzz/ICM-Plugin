# Room Contract — the room's `CONTEXT.md`

The room contract **is** the room's `CONTEXT.md`. There is no separate contract file. The agent reads it
and knows exactly what to load, what to produce, and where to put the result. Routing only — no reference
content lives here (that's Layer 3). Keep it short and concise ~80 lines, more than that, consider migrating info into the docs.

## The shape

```markdown
# <NN-name> — <one line: what this room transforms>

> <one-line scope + position in the pipeline, or "parallel capability">.

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Previous room | `../<NN-prev>/v<N>/<artifact>` | Full file | the artifact to work from |
| Reference | `../../docs/<file>.md` | "<section>" through "<section>" | <what it gives> |
<!-- Name the SECTION to load, not just the file (selective routing). -->

## Process
1. <concrete step, action verb>
2. ...
N. Drop `_handoff`; if gate=human, `_awaiting-human`; save output to the run folder.

## Checkpoints   (creative rooms only — delete if linear)
| After step | Agent presents | Human decides |
|------------|----------------|---------------|
| <#> | <options / draft> | <direction> |

## Audit   (creative / build rooms — delete if pure conversion)
| Check | Pass condition |
|-------|----------------|
| <name> | <unambiguous pass> |
| Upstream-brief trace | output still satisfies the brief that fed this room |

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| <name> | `projects/<run>/<NN-name>/v<N>/<file>` | <format> |

## Done when
- <concrete, unambiguous checklist — no "when it feels right">

## Hand-off
<what the next room consumes; the marker dropped>.

## Boundaries
Writes only its run output + `docs/memory/`. Drops markers; never writes machine state.
**NEVER modify** (never touches): <other rooms, other runs, Layer 3 during a run, the canonical docs without a CR>.

## Tools
Read `tools.json` first — it lists this room's tools (`toolname` · `tool-path` · `when-to-use` · `how-to-use`).
```

## Why these sections

- **Inputs** make context-loading explicit — the agent doesn't guess what to read.
- **Process** is a recipe a human could follow without the agent. If you can't write it as individual steps, the room
  does too much (split it).
- **Checkpoints / Audit** put human steering and a quality gate where they belong (creative work).
- **Outputs / Done-when / Hand-off** define the artifact and when the room is finished.
- **Boundaries** — the never-empty "NEVER modify" line is what prevents one room from corrupting another.

## Sub-rooms and the `NN.0` review

A room is one capability. When a subprocess genuinely ramifies, the room nests **sub-rooms**
(`NN.n-<name>`), each with its own `CONTEXT.md` + `docs/` — nestable by need, no depth cap. A room with
sub-rooms carries a routing table for them in its `CONTEXT.md` (see `ROUTING.md`); a leaf room just states
its contract.

A **checkpoint review is itself a documented sub-room**, `NN.0`. It is not an inline afterthought: it has a
`CONTEXT.md` (what it checks) and a `docs/` that states **how the review is done** — the pass conditions, the
upstream-brief trace, what gets escalated. `NN.0` runs at every checkpoint (not only at the end), despite
the `.0` number; `NN.1+` are the productive sub-rooms. A room's own `## Audit` table is the lightweight,
in-room version of this; a full `NN.0` sub-room is warranted when the review itself needs steps + memory.

## What NOT to put here

The voice guide, brand identity, or any reference material (lives in Layer 3, referenced from Inputs).
Agent personality (inherited from root `AGENTS.md`). If the contract exceeds ~80 lines, you're inlining
reference material — extract it to `docs/`. More broadly: **any workspace file over ~200 lines is flagged
to be split via a Change Request** (the `janitor` room handles the split + re-points the references); a
contract should never grow there in the first place.
