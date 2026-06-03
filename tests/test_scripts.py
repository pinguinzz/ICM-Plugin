"""Tests for the ICM checker (icm_check.py).

Run from the plugin root:
    python -m unittest discover tests

Stdlib only. No pytest required.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "scripts"
EXAMPLE = PLUGIN_ROOT / "examples" / "content-creator-demo"


def run(*args: str) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "icm_check.py"), *args],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    return r.returncode, r.stdout, r.stderr


def run_json(*args: str) -> tuple[int, dict, str]:
    rc, out, err = run(*args, "--json")
    return rc, (json.loads(out) if out.strip() else {}), err


def write_min_workspace(root: Path, go_to: str = "01-research/") -> None:
    """A minimal valid ICM workspace with one room and a resolvable routing pointer."""
    (root / "01-research").mkdir(parents=True)
    (root / "01-research" / "CONTEXT.md").write_text("# 01-research\n\nRoom.\n", encoding="utf-8")
    (root / "AGENTS.md").write_text(
        "# WS\n\n## Routing\n\n| Task | Go to |\n|---|---|\n"
        f"| Research | `{go_to}` |\n| Method | (here) |\n",
        encoding="utf-8",
    )


class TestCheckerClean(unittest.TestCase):

    def test_example_demo_is_clean(self):
        rc, data, err = run_json(str(EXAMPLE))
        self.assertEqual(rc, 0, err)
        self.assertEqual(data["errors"], [], data["errors"])

    def test_minimal_workspace_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)
            rc, data, err = run_json(str(root))
            self.assertEqual(rc, 0, err)
            self.assertEqual(data["errors"], [])


class TestInvariantViolations(unittest.TestCase):

    def test_docs_dash_name_antipattern(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)
            (root / "01-research" / "docs-research").mkdir()
            rc, data, _ = run_json(str(root))
            self.assertEqual(rc, 1)
            self.assertTrue(any("docs-<name>" in e for e in data["errors"]), data["errors"])

    def test_emoji_in_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)
            (root / "0\U0001F600-bad").mkdir()
            rc, data, _ = run_json(str(root))
            self.assertEqual(rc, 1)
            self.assertTrue(any("emoji" in e for e in data["errors"]), data["errors"])

    def test_broken_routing_pointer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root, go_to="99-missing/")
            rc, data, _ = run_json(str(root))
            self.assertEqual(rc, 1)
            self.assertTrue(any("routing pointer" in e for e in data["errors"]), data["errors"])

    def test_here_meta_marker_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)  # has a "(here)" row
            rc, data, _ = run_json(str(root))
            self.assertEqual(rc, 0)
            self.assertFalse(any("routing pointer" in e for e in data["errors"]))


class TestGuidelineWarnings(unittest.TestCase):

    def test_oversized_context_warns_not_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)
            big = "\n".join(f"line {i}" for i in range(120))
            (root / "01-research" / "CONTEXT.md").write_text("# 01-research\n" + big, encoding="utf-8")
            rc, data, _ = run_json(str(root))
            self.assertEqual(rc, 0, "oversize is a warning, not an error")
            self.assertTrue(any("CONTEXT.md >" in w for w in data["warnings"]), data["warnings"])

    def test_strict_fails_on_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_min_workspace(root)
            big = "\n".join(f"line {i}" for i in range(250))
            (root / "01-research" / "notes.md").write_text(big, encoding="utf-8")
            rc, _, _ = run(str(root), "--strict")
            self.assertEqual(rc, 1, "--strict should fail on warnings")


if __name__ == "__main__":
    unittest.main(verbosity=2)
