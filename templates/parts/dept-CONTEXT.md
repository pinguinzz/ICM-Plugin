# {{DEPT_NAME}} — department (L2)

> {{ONE_LINE_DEPT_PURPOSE}}

## Work pattern

**{{SEQUENTIAL_OR_PARALLEL}} pipeline.** {{PATTERN_RATIONALE}}
<!-- Sequential: rooms hand off in order via `projects/<run>/<NN-room>/`. -->
<!-- Parallel: capability rooms run independently via room-local `workbench-<id>/`. -->

## Routing (internal)

| Task | Go to |
|------|-------|
{{ROUTING_ROWS}}

## Map

```
{{DEPT_NAME}}/
├── CONTEXT.md          this file (L2)
├── docs/               L3 — shared department references + memory
└── {{NN-room}}/ ...    rooms (each: CONTEXT.md + docs/ + optional sub-rooms NN.n-<name>)
```

## Boundaries

Acts only through its rooms. Never edits another department's folders. Structural change → CR.
