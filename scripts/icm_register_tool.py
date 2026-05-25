"""Register a new tool (skill) into the workspace's routing table.

Usage:
    python icm_register_tool.py \\
        --workspace WORKSPACE_ROOT \\
        --tool-name NAME \\
        --tool-description "one-line description" \\
        [--target-folder skills/]   # where the SKILL.md lives, relative to workspace
        [--wire-into "task substring"]  # routing row whose Skills column should be updated

Creates `<workspace>/<target-folder>/<NAME>/SKILL.md` from the plugin's tool-SKILL.md template
(with placeholders filled in), and appends the tool name to the matching row's `Skills` column.

If --wire-into is omitted, only creates the SKILL.md (does not modify AGENTS.md routing).

Exit codes:
    0 = ok
    1 = error
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    CANONICAL_AGENT_FILE, emit_json, die,
    find_workspace_root, parse_routing_table, read_text,
    render_routing_table, replace_routing_section,
)


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TOOL_TEMPLATE = PLUGIN_ROOT / "templates" / "parts" / "tool-SKILL.md"


def make_skill_file(target: Path, name: str, description: str, workspace_path: str) -> str:
    src = read_text(TOOL_TEMPLATE)
    filled = (src
              .replace("{{TOOL_NAME}}", name)
              .replace("{{TOOL_DISPLAY_NAME}}", name)
              .replace("{{ONE_LINE_DESCRIPTION_TRIGGERS_THIS_SKILL}}", description)
              .replace("{{WORKSPACE_PATH}}", workspace_path)
              .replace("{{WHEN_TO_USE}}", "TODO: describe when to use this tool.")
              .replace("{{WHAT_IT_DOES}}", "TODO: describe what it does.")
              .replace("{{INPUT_1}}", "TODO")
              .replace("{{INPUT_2}}", "TODO")
              .replace("{{STEP_1}}", "TODO")
              .replace("{{STEP_2}}", "TODO")
              .replace("{{STEP_3}}", "TODO")
              .replace("{{WHAT_IT_PRODUCES}}", "TODO"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(filled, encoding="utf-8")
    return target.as_posix()


def wire_into_routing(agents_md: Path, tool_name: str, task_substring: str) -> bool:
    text = read_text(agents_md)
    rows = parse_routing_table(text)
    if not rows:
        return False
    needle = task_substring.lower()
    matched = False
    for row in rows:
        if needle in row.task.lower():
            existing = [s.strip() for s in row.skills.split(",") if s.strip() not in ("", "—", "-")]
            if tool_name not in existing:
                existing.append(tool_name)
            row.skills = ", ".join(existing) if existing else "—"
            matched = True
    if not matched:
        return False
    new_text = replace_routing_section(text, render_routing_table(rows))
    agents_md.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--tool-name", required=True)
    ap.add_argument("--tool-description", required=True)
    ap.add_argument("--target-folder", default="skills")
    ap.add_argument("--wire-into", default=None, help="Substring of the Task column to wire this tool into")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()
    if not ws.exists():
        die(f"Workspace not found: {ws}", code=1)

    root = find_workspace_root(ws)
    if root is None:
        die(f"{ws} is not inside an ICM workspace.", code=1)

    target_folder = (ws / args.target_folder).resolve()
    skill_path = target_folder / args.tool_name / "SKILL.md"
    if skill_path.exists():
        die(f"Skill already exists at {skill_path}", code=1)

    written = make_skill_file(
        skill_path,
        args.tool_name,
        args.tool_description,
        ws.relative_to(root).as_posix() or ".",
    )

    wired = False
    if args.wire_into:
        agents_md = root / CANONICAL_AGENT_FILE
        if agents_md.exists():
            wired = wire_into_routing(agents_md, args.tool_name, args.wire_into)

    emit_json({
        "workspace_root": root.as_posix(),
        "skill_path": written,
        "wired_into_routing": wired,
        "next_steps": [
            f"Edit {written} and fill in the TODO sections.",
            "Run icm_remap.py to validate the routing table.",
        ],
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
