"""Detect whether a given path is an ICM workspace.

Usage:
    python icm_detect.py [PATH]

Outputs JSON to stdout describing what was found.
Exit codes:
    0 = is an ICM workspace
    1 = path doesn't exist
    2 = not an ICM workspace
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    AGENT_FILES, CANONICAL_AGENT_FILE, STUB_FILES,
    detect_layers, find_stages, find_workspaces,
    find_workspace_root, is_stub, read_text, count_tokens,
    emit_json, die,
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".", help="Path to inspect (default: cwd)")
    args = ap.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        die(f"Path does not exist: {target}", code=1)

    root = find_workspace_root(target)
    is_icm = root is not None

    result: dict = {
        "input_path": target.as_posix(),
        "is_icm_workspace": is_icm,
        "workspace_root": root.as_posix() if root else None,
    }

    if not is_icm:
        result["reason"] = (
            "No AGENTS.md / CLAUDE.md / GEMINI.md / .cursorrules found at this folder "
            "or any ancestor. Run /ICM-set-up to scaffold."
        )
        emit_json(result)
        return 2

    # Inspect the workspace
    layers = detect_layers(root)
    stages = find_stages(root)
    workspaces = find_workspaces(root)

    # Agent-file inventory
    agent_inventory = {}
    for name in AGENT_FILES:
        p = root / name
        if p.exists():
            txt = read_text(p)
            agent_inventory[name] = {
                "exists": True,
                "tokens": count_tokens(txt),
                "is_stub": is_stub(p) if name in STUB_FILES else False,
            }
        else:
            agent_inventory[name] = {"exists": False}

    canonical = agent_inventory.get(CANONICAL_AGENT_FILE, {})
    has_canonical = bool(canonical.get("exists"))

    # Check stub fidelity (stubs should point to AGENTS.md, not duplicate content)
    stub_warnings = []
    for name in STUB_FILES:
        info = agent_inventory.get(name, {})
        if info.get("exists") and not info.get("is_stub"):
            if has_canonical:
                stub_warnings.append(
                    f"{name} exists but is not a stub pointing to AGENTS.md. "
                    f"Risk: divergent content."
                )

    # Determine workspace style
    if stages:
        style = "pipeline"
    elif workspaces:
        style = "workspaces"
    elif has_canonical:
        style = "flat"
    else:
        style = "unknown"

    result.update({
        "style": style,
        "agent_files": agent_inventory,
        "stub_warnings": stub_warnings,
        "layer_counts": {f"layer_{k}": len(v) for k, v in layers.items()},
        "stages": [s.__dict__ for s in stages],
        "workspaces": [w.__dict__ for w in workspaces],
    })

    emit_json(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
