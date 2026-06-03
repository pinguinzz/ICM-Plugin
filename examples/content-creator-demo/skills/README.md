# Workspace Skills

This folder holds skills wired into this specific workspace. Skills here are loaded only when the room's
`CONTEXT.md` calls for them — not globally.

To add a skill, run `/icm:new` (scope: a tool/skill) or author a `SKILL.md` from the plugin's
`templates/parts/tool-SKILL.md`, declare it in the room's `tools.json`, and vendor it with skills-sync.
