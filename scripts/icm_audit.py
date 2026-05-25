"""Audit an ICM workspace for structural issues.

Usage:
    python icm_audit.py [PATH]

Reports (JSON to stdout):
    - oversized CONTEXT.md files
    - missing CONTEXT.md in stages/workspaces
    - missing references/ or output/ folders in stages
    - non-stub compatibility files
    - naming violations (stage prefix format)
    - broken pointers in routing table (Go to / Read paths that don't exist)

Exit codes:
    0 = clean
    1 = error (path missing / not an ICM workspace)
    2 = issues found (non-fatal, but worth fixing)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    CANONICAL_AGENT_FILE, STAGE_PREFIX_RE, STUB_FILES,
    count_tokens, detect_layers, emit_json, die,
    find_stages, find_workspace_root, find_workspaces,
    is_stub, parse_routing_table, read_text,
)


ROOT_AGENTS_MAX_TOKENS = 1000   # ~50 lines
WORKSPACE_CONTEXT_MAX_TOKENS = 600
STAGE_CONTEXT_MAX_TOKENS = 600


def audit(root: Path) -> dict:
    issues: list[dict] = []

    # 1. Canonical agent file
    canonical = root / CANONICAL_AGENT_FILE
    if not canonical.exists():
        issues.append({
            "severity": "error",
            "code": "missing_canonical",
            "where": CANONICAL_AGENT_FILE,
            "message": "No AGENTS.md at workspace root. The canonical agent contract is missing.",
        })

    # 2. Stub fidelity
    for name in STUB_FILES:
        p = root / name
        if p.exists() and not is_stub(p):
            issues.append({
                "severity": "warn",
                "code": "non_stub_compat",
                "where": name,
                "message": f"{name} should be a one-liner pointing to AGENTS.md. Found content.",
            })

    # 3. Root AGENTS.md size
    if canonical.exists():
        tokens = count_tokens(read_text(canonical))
        if tokens > ROOT_AGENTS_MAX_TOKENS:
            issues.append({
                "severity": "warn",
                "code": "oversized_root",
                "where": CANONICAL_AGENT_FILE,
                "message": f"{CANONICAL_AGENT_FILE} is ~{tokens} tokens (max {ROOT_AGENTS_MAX_TOKENS}). Extract detail into workspace CONTEXT.md files.",
                "tokens": tokens,
            })

    # 4. Root CONTEXT.md exists (Layer 1)
    root_ctx = root / "CONTEXT.md"
    if not root_ctx.exists():
        issues.append({
            "severity": "warn",
            "code": "missing_root_context",
            "where": "CONTEXT.md",
            "message": "No root CONTEXT.md (Layer 1).",
        })

    # 5. Stages
    stages = find_stages(root)
    for s in stages:
        if not s.has_context:
            issues.append({
                "severity": "error",
                "code": "stage_missing_context",
                "where": s.folder,
                "message": f"Stage {s.folder} has no CONTEXT.md. Stage contract missing.",
            })
        else:
            if s.context_tokens > STAGE_CONTEXT_MAX_TOKENS:
                issues.append({
                    "severity": "warn",
                    "code": "oversized_stage_context",
                    "where": f"{s.folder}/CONTEXT.md",
                    "message": f"Stage CONTEXT.md is ~{s.context_tokens} tokens (max {STAGE_CONTEXT_MAX_TOKENS}).",
                    "tokens": s.context_tokens,
                })
        if not s.has_output:
            issues.append({
                "severity": "warn",
                "code": "stage_missing_output",
                "where": s.folder,
                "message": f"Stage {s.folder} has no output/ folder.",
            })
        # naming check
        m = STAGE_PREFIX_RE.match(Path(s.folder).name)
        if not m:
            issues.append({
                "severity": "warn",
                "code": "stage_naming",
                "where": s.folder,
                "message": f"Stage folder name does not match `NN-name` pattern.",
            })

    # 6. Workspaces (non-pipeline)
    workspaces = find_workspaces(root)
    for w in workspaces:
        if not w.has_context:
            issues.append({
                "severity": "warn",
                "code": "workspace_missing_context",
                "where": w.folder,
                "message": f"Workspace {w.folder} has no CONTEXT.md.",
            })
        else:
            if w.context_tokens > WORKSPACE_CONTEXT_MAX_TOKENS:
                issues.append({
                    "severity": "warn",
                    "code": "oversized_workspace_context",
                    "where": f"{w.folder}/CONTEXT.md",
                    "message": f"Workspace CONTEXT.md is ~{w.context_tokens} tokens (max {WORKSPACE_CONTEXT_MAX_TOKENS}).",
                    "tokens": w.context_tokens,
                })

    # 7. Routing table pointers
    if canonical.exists():
        rows = parse_routing_table(read_text(canonical))
        for row in rows:
            # `go_to` may be a relative path; check existence
            target_path = row.go_to.strip().strip("`").strip("/")
            if target_path and target_path not in ("(here)", "—", "-"):
                if not (root / target_path).exists():
                    issues.append({
                        "severity": "error",
                        "code": "routing_broken_pointer",
                        "where": CANONICAL_AGENT_FILE,
                        "message": f"Routing row '{row.task}' → '{target_path}' does not exist.",
                    })
            # `read` files
            for f in [x.strip().strip("`") for x in row.read.split(",") if x.strip() and x.strip() not in ("—", "-")]:
                # `read` paths can be relative to the `go_to` folder
                base = (root / target_path) if target_path and target_path not in ("(here)", "—", "-") else root
                candidate = (base / f).resolve()
                # ignore obviously external references like "the ICM plugin's docs/"
                if "ICM plugin" in f or f.startswith("..") or " " in f:
                    continue
                if not candidate.exists():
                    issues.append({
                        "severity": "warn",
                        "code": "routing_broken_read",
                        "where": CANONICAL_AGENT_FILE,
                        "message": f"Routing row '{row.task}' reads missing file: {f} (resolved: {candidate.relative_to(root) if candidate.is_relative_to(root) else candidate})",
                    })

    # Summary
    summary = {
        "errors": sum(1 for i in issues if i["severity"] == "error"),
        "warnings": sum(1 for i in issues if i["severity"] == "warn"),
        "info": sum(1 for i in issues if i["severity"] == "info"),
    }

    return {
        "workspace_root": root.as_posix(),
        "summary": summary,
        "layer_counts": {f"layer_{k}": len(v) for k, v in detect_layers(root).items()},
        "stages_count": len(stages),
        "workspaces_count": len(workspaces),
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".")
    args = ap.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        die(f"Path does not exist: {target}", code=1)

    root = find_workspace_root(target)
    if root is None:
        die(f"{target} is not inside an ICM workspace.", code=1)

    result = audit(root)
    emit_json(result)
    if result["summary"]["errors"] > 0 or result["summary"]["warnings"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
