# Routing — The Spine of an ICM Workspace

The routing table lives in the workspace's root `AGENTS.md`. It tells the agent: for THIS kind of task, go HERE and read THESE files.

## The shape

```markdown
## Routing

|Task|Go to|
|---|---|
|Research a topic|rooms/01-research/|
|Draft a script|rooms/02-script/|
|Build an animation|rooms/03-production/|
|Debug the pipeline|(here)|
```

## Columns

- **Task** — phrased the way a user would describe the work in natural language. Keep it short.
- **Go to** — relative path from workspace root.

## How the agent uses it

1. Reads `AGENTS.md`.
2. Matches the user's request to a row.
3. Changes working context to the `Go to` folder.

## When to update it

- A new room is added → new row.
- A room is renamed → update column 2.

Run `/icm:remap` to regenerate the table from current folder reality. The script reads what's actually on disk and rewrites the table.

## Anti-patterns

- **Routing by AI inference** — don't say "agent figures out where to go." It will guess wrong. Write the row.
- **Skipping the table** — without it, every task starts from zero and the agent has to discover the structure each time.

## Multiple routing tables?

Workspaces with sub-workspaces can have a second routing table inside the workspace's own `CONTEXT.md`. Same shape. Same rules. Routes within that workspace only.
