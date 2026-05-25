# Routing — The Spine of an ICM Workspace

The routing table lives in the workspace's root `AGENTS.md`. It tells the agent: for THIS kind of task, go HERE and read THESE files.

## The shape

```markdown
## Routing

| Task | Go to | Read | Skills |
|------|-------|------|--------|
| Research a topic | stages/01-research/ | CONTEXT.md | web-search |
| Draft a script | stages/02-script/ | CONTEXT.md, ../shared/voice.md | — |
| Build an animation | stages/03-production/ | CONTEXT.md, ../shared/component-library.md | remotion |
| Debug the pipeline | (here) | docs/CONVENTIONS.md | — |
```

## Columns

- **Task** — phrased the way a user would describe the work in natural language. Keep it short.
- **Go to** — relative path from workspace root.
- **Read** — comma-separated list of files the agent loads in that folder. The folder's `CONTEXT.md` is almost always first.
- **Skills** — comma-separated names of skills the agent may invoke for that task. `—` if none.

## How the agent uses it

1. Reads `AGENTS.md`.
2. Matches the user's request to a row.
3. Changes working context to the `Go to` folder.
4. Loads the `Read` files.
5. Optionally invokes the `Skills`.

The routing table is the **only** orchestration the system needs. No code. No framework.

## When to update it

- A new stage is added → new row.
- A stage is renamed → update column 2.
- A reference file is added → update column 3 for the relevant rows.
- A skill is wired in → update column 4.

Run `/icm:remap` to regenerate the table from current folder reality. The script reads what's actually on disk and rewrites the table.

## Anti-patterns

- **Routing by AI inference** — don't say "agent figures out where to go." It will guess wrong. Write the row.
- **Loading globally** — don't write "always read everything in `/shared/`." Each row picks specific files.
- **Skipping the table** — without it, every task starts from zero and the agent has to discover the structure each time.

## Multiple routing tables?

Workspaces with sub-workspaces can have a second routing table inside the workspace's own `CONTEXT.md`. Same shape. Same rules. Routes within that workspace only.
