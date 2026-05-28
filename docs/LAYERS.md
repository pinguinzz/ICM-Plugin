# The 5 Layers

ICM organizes context as a hierarchy. Each layer answers one question. Each layer has its own file and lives in its own place on disk. An agent loads only the layers it needs for the task at hand.

|Layer|Name|Question it answers|File / Folder|Typical size|Changes|
|---|---|---|---|---|---|
|0|Frontdoor|Where am I? (global identity, agent contract)|\`AGENTS.md\` at workspace root (+ stubs: \`CLAUDE.md\`, \`GEMINI.md\`, \`.cursorrules\`)|\~800 tokens|Never (after setup)|
|1|Reception|Where do I go? (workspace routing)|\`CONTEXT.md\` at workspace root|\~300 tokens|Setup only|
|2|Rooms|What work do I do? (the workspace contract)|`CONTEXT.md` in each room / workspace folder|200–500 tokens|Setup only|
|3|HowtoWork|What are the rules? (work references and rules)|`references/`, `folders`, `_config/`, `shared/`, `docs`|500–2k tokens|Per workspace|
|4|Product|What am I working on? (hand's on work forder)|`output/`,`output/`, `drafts/`, `builds/`|Variable|Every run|

## Why layers

If an agent loads everything in the project, it spends tokens reading irrelevant context, and the relevant context gets buried.
If an agent loads only the right layers for its current job, it stays sharp.

## The split that matters most: Layer 3 vs Layer 4

- **Layer 3 is the factory.** Stable rules. Voice guides. Conventions. House style. Don't edit during a run.
- **Layer 4 is the product.** The artifact this particular run produces. Edit and discard freely.
Mixing them is the most common ICM mistake.

## How agents enter

1. Enter the workspace. Agent reads `AGENTS.md` (Layer 0).
2. `AGENTS.md` points to root `CONTEXT.md` (Layer 1) and the routing table.
3. Routing table sends the agent to a specific workspace / room folder.
4. Room `CONTEXT.md` (Layer 2) tells it which references to load (Layer 3) and where to write (Layer 4).

Each step narrows the context window. The agent never carries more than it needs.

## Reading order

```
AGENTS.md (Layer 0)
    └──> CONTEXT.md (Layer 1) [routing table picks one]
        └──> workspace/n-room/CONTEXT.md (Layer 2)
            └──> workspace/n-room/references/* (Layer 3)
                └──> workspace/n-room/output/* (Layer 4)
```

## Token budget

A well-built ICM workspace lets a single agent specialize per room by reading ~5k tokens instead of ~40k. The model is the same; only the context changes.
