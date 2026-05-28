---
name: dispatch-subagent
description: Generic ICM-aware subagent dispatch. MVP supports type "reviewer" (auto-review pre-pass). Main agents invoke this to obtain transitory feedback before requesting human review, with model selection (haiku/sonnet/opus) proportional to the workload's expected value (`retorno_esperado` tier). Subagent does NOT create junctions, write markers, or invoke icm-compact — it writes transitory feedback that the main agent reads and removes. Pairs with `icm:new-pipeline` (the broader pattern).
---

# dispatch-subagent — Generic subagent dispatch

## When to invoke

A main agent (writer, editor, or any room-level executor) wants **auto-review** before creating an `_aguardando_revisao` marker for the human. Typical cases:

- `retorno_esperado >= alto` (or the equivalent high-value tier from the workspace's `config.json`) — worth spending a reviewer to pre-validate.
- Self-assessment is low (the agent senses a gap in the output).
- Output is particularly novel (no close few-shot match in `exemplos/aprovados/` or equivalent).

## Do NOT invoke if:

- You are a subagent yourself (subagents do not call subagents).
- You are not at a clear sub-room transition (auto-review only makes sense AFTER generating the output, BEFORE marking `_aguardando_revisao`).

## Args (infer from context)

- `tipo` — currently the only valid value is `reviewer`. Extensible to `linter`, `safety-checker`, etc.
- `model` — `haiku` (default) | `sonnet` | `opus`. Recommendation by tier (read from `config.tiers.<tier>.models.reviewer` or equivalent in the workspace's config):
  - low/medium tier → `haiku`
  - high tier → `sonnet`
  - critical tier → `opus`
  - Manual override allowed if you sense you need more (or less) depth.
- `alvo` — absolute path of the sub-room output to review (e.g. `<workspace>/<rooms-root>/<room>/<unit>/<sub_n>/`).

## Process (executed by the main agent)

1. Build the ICM-aware prompt for the subagent:

```
You are an ICM-aware reviewer subagent, model {model}.

CONTEXT:
- Workspace: {workspace name from AGENTS.md identity}
- You were dispatched by a main agent operating in an ICM room room.
- Mission: review the output at <alvo absolute path>.

INPUTS (read all):
- {workspace_root}/AGENTS.md
- Layer 3 identity files relevant to this output (paths passed by the main agent)
- Global Layer 0 memory file if the workspace defines one
- Top-K filtered learnings from the room's `memoria/learnings.jsonl`
- The TARGET in <alvo absolute path>

OUTPUT:
- Create `<alvo absolute>/revisao_provisoria.md` (or the equivalent transitory file the workspace uses) with actionable feedback.
- Suggested structure: bullet list of problems + bullet list of suggested fixes.
- Tone: constructive, specific, citing workspace identity files when applicable.

MECHANICAL CONSTRAINTS (CRITICAL):
- YOU ARE NOT THE MAIN AGENT. You are transitory.
- DO NOT create any junction (`campanha-em-foco-<id>/` or any other instance pointer). Read everything via absolute paths.
- DO NOT write any marker (`_concluido`, `_rejeitado`, `_aguardando_revisao`).
- DO NOT update `_room.json`, `learnings.jsonl`, `preferencias.md`, or any memory artifact.
- DO NOT invoke `icm-compact`.
- DO NOT invoke `dispatch-subagent` (no recursive dispatch).
- Only output: the `revisao_provisoria.md`. Terminate by returning "review complete".
```

2. Invoke the `Agent` tool:
   - `subagent_type`: `general-purpose`
   - `model`: pass `claude-haiku-4-5-20251001` | `claude-sonnet-4-6` | `claude-opus-4-7` per the `model` arg
   - `prompt`: the filled-in prompt above
   - `description`: "Auto-review {tipo} at {alvo}"

3. Wait for the subagent to return.

4. Post-return:
   - Read `<alvo>/revisao_provisoria.md`.
   - Decide apply/ignore (record rationale briefly in your own scratch).
   - Append entry to `<alvo>/revisao.json.auto_review[]` (sidecar pattern — see `icm:new-pipeline`):
     ```json
     {
       "ts": "<now ISO>",
       "model": "<model used>",
       "tipo": "reviewer",
       "feedback": "<feedback summary>",
       "aplicado": true | false,
       "diff_resumido": "<what changed if applied>"
     }
     ```
   - **Remove** `<alvo>/revisao_provisoria.md` (transitory).
   - Continue your main loop.

## Anti-patterns

- ❌ Dispatching a subagent when you ARE a subagent.
- ❌ Recursive dispatch (subagent invoking `dispatch-subagent`).
- ❌ Not removing `revisao_provisoria.md` after processing (leaves garbage in the unit's folder).
- ❌ Not recording the entry in `revisao.json.auto_review[]` when you applied feedback (loses traceability).
- ❌ Dispatching and then ignoring the feedback without recording `aplicado: false` (loses learning signal).

## Related

- `icm:new-pipeline` — the broader pattern this skill fits into (multi-room pipelines with granular review gates, sidecar `revisao.json`, tier-aware execution).
- `icm:icm` — the main meta-skill (loaded on entering any ICM workspace).
