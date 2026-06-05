# {{NN-NAME}} — {{ONE_LINE_WHAT_THIS_ROOM_TRANSFORMS}}

> {{SCOPE_AND_POSITION}}  <!-- position in the pipeline, or "parallel capability". -->
<!-- A room may nest sub-rooms NN.n-<name> (recursion by need). NN.0 = QA/auto-review (runs at checkpoints). -->

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| {{SOURCE_1}} | {{PATH_1}} | {{SECTION_1}} | {{WHY_1}} |

## Process
1. {{STEP_1}}
N. Drop `_handoff`; if gate=human, `_awaiting-human`; save output to the run folder.

## Checkpoints   (creative rooms only — delete if linear)
| After step | Agent presents | Human decides |
|------------|----------------|---------------|
| {{#}} | {{OPTIONS}} | {{DIRECTION}} |

## Audit   (creative/build rooms — delete if pure conversion)
| Check | Pass condition |
|-------|----------------|
| {{CHECK}} | {{PASS}} |
| Upstream-brief trace | output still satisfies the brief that fed this room |

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| {{NAME}} | `{{OUTPUT_PATH}}` | {{FORMAT}} |

## Done when
- {{CONCRETE_CRITERION}}

## Hand-off
{{WHAT_NEXT_ROOM_CONSUMES}}; marker dropped.

## Boundaries
Writes only its run output + `docs/memory/`. Drops markers; never writes machine state. **NEVER modify**:
{{NEVER_TOUCHES}}.

## Tools
Read `tools.json` first ({{TOOLS_OR_"none"}}).
