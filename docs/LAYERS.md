# The 5 Layers

ICM organizes context as a hierarchy. Each layer answers one question. Each layer has its own file and lives in its own place on disk. An agent loads only the layers it needs for the task at hand.

| Layer | Question it answers | File / Folder | Typical size | Changes |
|------:|---|---|---|---|
| 0 | Where am I? (global identity, agent contract) | `AGENTS.md` at workspace root (+ stubs: `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) | ~800 tokens | Never (after setup) |
| 1 | Where do I go? (workspace routing) | `CONTEXT.md` at workspace root | ~300 tokens | Setup only |
| 2 | What do I do? (the stage contract) | `CONTEXT.md` in each stage / workspace folder | 200–500 tokens | Setup only |
| 3 | What are the rules? (stable references) | `references/` folders, `_config/`, `shared/` | 500–2k tokens | Per workspace |
| 4 | What am I working on? (the run) | `output/`, `drafts/`, `builds/` | Variable | Every run |

## Why layers

If an agent loads everything in the project, it spends tokens reading irrelevant context, and the relevant context gets buried (the "lost in the middle" problem).

If an agent loads only the right layers for its current job, it stays sharp.

## The split that matters most: Layer 3 vs Layer 4

- **Layer 3 is the factory.** Stable rules. Voice guides. Conventions. House style. Don't edit during a run.
- **Layer 4 is the product.** The artifact this particular run produces. Edit freely. Discard freely.

Mixing them is the most common ICM mistake.

## How agents enter

1. Open the workspace. Agent reads `AGENTS.md` (Layer 0).
2. `AGENTS.md` points to root `CONTEXT.md` (Layer 1) and the routing table.
3. Routing table sends the agent to a specific workspace / stage folder.
4. Stage `CONTEXT.md` (Layer 2) tells it which references to load (Layer 3) and where to write (Layer 4).

Each step narrows the context window. The agent never carries more than it needs.

## Reading order

```
AGENTS.md (Layer 0)
    │
    └──> CONTEXT.md (Layer 1)
              │
              └──> [routing table picks one]
                          │
                          └──> stages/0X-task/CONTEXT.md (Layer 2)
                                       │
                                       ├──> stages/0X-task/references/* (Layer 3)
                                       └──> stages/0X-task/output/* (Layer 4)
```

## Token budget

A well-built ICM workspace lets a single agent specialize per stage by reading ~5k tokens instead of ~40k. The model is the same; only the context changes.
