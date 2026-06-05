---
name: {{TOOL_NAME}}
description: {{ONE_LINE_DESCRIPTION_TRIGGERS_THIS_SKILL}}
---

# {{TOOL_DISPLAY_NAME}}

## When to use

{{WHEN_TO_USE}}

## What it does

{{WHAT_IT_DOES}}

## Inputs it expects

- {{INPUT_1}}
- {{INPUT_2}}

## How to use

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}

## Outputs

{{WHAT_IT_PRODUCES}}

## Wired into

Lives in the central store under `<root>/.claude/`; the room activates it by adding an entry to its
`tools.json` (`toolname` · `tool-path` relative to workspace root · `when-to-use` · `how-to-use`). The
room's `CONTEXT.md` **Tools** section tells the agent to read `tools.json` first.
