# Routing — the spine of an ICM workspace

Root `AGENTS.md` (L0) says what this place is, what it does and how to enter it, then points to the routing table that lives in the workspace's root **`CONTEXT.md`** (L1 = maps + where to go). It tells the agent: for *THIS* kind of task, go *HERE*. Departments carry their own sub-routing tables in their `CONTEXT.md`.

## The shape

```markdown
## Routing

| Task | Go to |
|------|-------|
| Research a topic | `01-research/` |
| Draft a script | `02-script/` |
| Maintain the workspace / change structure | `maintenance/` |
| Methodology question | (here) |
```

## Columns

- **Task** — phrased the way a user describes the work in natural language. Keep it short.
- **Go to** — a path relative to this file's folder, or `(here)` (a meta row: this file answers it, no
  folder to navigate to).

## How the agent uses it

1. Reads `AGENTS.md` (identity + base rules), then root `CONTEXT.md` (the routing table).
2. Matches the user's request to a row.
3. Moves its working context to the `Go to` folder and reads that folder's `CONTEXT.md`.
4. If the target is a **department**, it has its own routing table — follow it to the actual room.

## Nested example (departments → rooms)

A clustered workspace routes twice. Root `CONTEXT.md`:

```markdown
| Produce a post (research → script → edit → package) | `dept-content/` |
| Track metrics | `dept-analytics/` |
```

Then `dept-content/CONTEXT.md` carries the inner table:

```markdown
| Research products | `01-research/` |
| Write the script | `02-script/` |
```

Same shape, same rules, scoped to that department.

## Sub-rooms (routing within a room)

Routing recurses with the structure. A **room** (`NN-name`) may hold **sub-rooms** (`NN.n-<name>`), and a
sub-room may hold its own (`NN.n.m-<name>`) — nestable by need, no depth cap. Each node carries a
`CONTEXT.md`; a node with children carries a routing table for them, exactly like a department:

```markdown
# 02-script — write the post script
| Frame the concept | `02.1-concept/` |
| Write the copy    | `02.2-copy/` |
| Review the script | `02.0-review/` |   (NN.0 = QA / auto-review)
```

The agent descends one routing hop at a time (dept → room → sub-room → …), reading each `CONTEXT.md` on the
way and loading nothing it doesn't name. A leaf room (no children) has no inner table — it just states its
contract.

## When to update it

- A new room is added → new row. A room is renamed → update the `Go to`.
- Keep meta rows (`(here)`) — they answer in place; they are not broken pointers.

## Anti-patterns

- **Routing by AI inference** — don't write "the agent figures out where to go." It guesses wrong. Write
  the row.
- **Skipping the table** — without it, every task starts from zero and the agent rediscovers the structure
  each time.
- **Shrinking the table on refresh** — never drop curated rows (incl. meta rows) when regenerating from
  disk; descend into numbered/nested subfolders so real rooms aren't missed.
