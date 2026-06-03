---
name: dispatch-subagent
description: Canonical ICM primitive — dispatch a subagent that spawns as a generic ICM agent. The subagent reads `AGENTS.md`, self-routes to a named room, finds its own data and output target, and completes the job. Use when you want work done in another room (e.g. a gated edit in the maintenance room) or a review pre-pass before requesting human review. Model (haiku/sonnet/opus) scales to the work's expected value. The dispatcher names WHERE (the room) and WHAT (the job); the subagent finds its own way.
---

# dispatch-subagent — spawn an ICM-aware subagent

The subagent is **a generic ICM agent**, not a special tool. You tell it WHERE (which room) and WHAT (the
job); it enters the workspace, reads `AGENTS.md`, routes to that room, reads the room `CONTEXT.md`, loads
the Inputs it names, does the work in that room's output target, and drops markers — exactly as any ICM
agent would. You do **not** pre-load its context; the frontdoor protocol does.

## Two canonical uses

1. **Worker** — dispatch to a room to do real work (most common: a **gated edit via the maintenance
   room**, or running a productive room). The subagent follows that room's contract: writes to the room's
   output target, drops the room's markers, honors its Boundaries. It is a full ICM agent.
2. **Reviewer** — an auto-review pre-pass before you request human review. The subagent is **transitory**:
   it reads via absolute paths and writes only a provisional review file; it creates no markers and no
   state. You read its feedback, apply or discard, record the decision, and remove the provisional file.

## When to invoke

- You need work completed in a room other than the one you're in (and that room is the right owner).
- `retorno_esperado`/value is high, self-assessment is low, or the output is novel → a reviewer pre-pass
  is worth it before the human gate.

## Do NOT invoke if

- You are a subagent yourself (no recursive dispatch).
- For a reviewer: you are not at a clear post-generation, pre-human-gate point.

## Args (infer from context)

- `mode` — `worker` | `reviewer`.
- `room` — the target room (worker) or the path to review (reviewer), as an **absolute path** or a routing
  target the subagent can resolve from `AGENTS.md`.
- `model` — `haiku` (default) | `sonnet` | `opus`, scaled to the work's value tier (read the workspace's
  `config` if it declares tiers): low/medium → haiku · high → sonnet · critical → opus. Model IDs:
  `claude-haiku-4-5-20251001` · `claude-sonnet-4-6` · `claude-opus-4-8`.

## Process

1. Build the subagent prompt (fill the braces):

```
You are an ICM agent dispatched into this workspace, model {model}, mode {mode}.

ENTRY (do this first):
- Read {workspace_root}/AGENTS.md, then root CONTEXT.md for routing. Match your mission to a Routing row
  and navigate to {room}.
  Read that room's CONTEXT.md and load ONLY the Inputs it names. Find your own data and output target.

MISSION:
- {one-paragraph statement of WHAT to accomplish}

IF mode=worker:
- Do the job per the room's contract. Write ONLY to that room's output target. Drop the room's markers.
  Honor its Boundaries. You are a full ICM agent — follow the structure exactly.

IF mode=reviewer (transitory):
- Review the TARGET at {room}. Read everything via absolute paths.
- Write ONLY `{room}/review_provisional.md` (problems + suggested fixes, specific, citing the workspace's
  Layer-3 identity files where relevant).
- DO NOT create junctions, markers (`_handoff`/`_done`/`_rejected`/`_awaiting-human`), or touch state/memory.
- DO NOT dispatch a subagent. Terminate by returning "review complete".
```

2. Invoke the `Agent` tool — `subagent_type: general-purpose`, `model:` per the arg, `prompt:` the filled
   text, `description:` "{mode} in {room}".
3. Wait for it to return.
4. **Post-return:**
   - *Worker:* verify the markers/output landed where the room contract says; continue your loop.
   - *Reviewer:* read `{room}/review_provisional.md`, decide apply/discard, record the decision in the
     run's review sidecar (e.g. `revisao.json`/`review.json` `auto_review[]`), **remove** the provisional
     file, then proceed to the human gate.

## Anti-patterns

- Dispatching when you ARE a subagent, or recursive dispatch.
- Pre-loading the subagent's room context yourself instead of letting it self-route (defeats the point).
- Reviewer leaving `review_provisional.md` behind, or applying feedback without recording it.
- Worker writing outside the target room's output target.

## Related

- `icm` — the meta-skill (the frontdoor protocol the subagent follows).
