"""End-to-end tests for the ICM helper scripts.

Run from the plugin root:
    python -m unittest discover tests
or:
    python tests/test_scripts.py

Stdlib only. No pytest required.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "scripts"
EXAMPLE = PLUGIN_ROOT / "examples" / "content-creator-demo"


def run_script(name: str, *args: str) -> tuple[int, str, str]:
    """Invoke a script and return (returncode, stdout, stderr)."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )
    return result.returncode, result.stdout, result.stderr


def run_json(name: str, *args: str) -> tuple[int, dict, str]:
    rc, out, err = run_script(name, *args)
    data = json.loads(out) if out.strip() else {}
    return rc, data, err


class TestDetect(unittest.TestCase):

    def test_detects_example_pipeline(self):
        rc, data, err = run_json("icm_detect.py", str(EXAMPLE))
        self.assertEqual(rc, 0, err)
        self.assertTrue(data["is_icm_workspace"])
        self.assertEqual(data["style"], "pipeline")
        self.assertEqual(len(data["stages"]), 3)
        # Every stage should have CONTEXT.md and output/
        for s in data["stages"]:
            self.assertTrue(s["has_context"], s)
            self.assertTrue(s["has_output"], s)

    def test_non_icm_folder_returns_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc, data, err = run_json("icm_detect.py", tmp)
            self.assertEqual(rc, 2, err)
            self.assertFalse(data["is_icm_workspace"])
            self.assertIsNone(data["workspace_root"])

    def test_stubs_recognized(self):
        rc, data, _ = run_json("icm_detect.py", str(EXAMPLE))
        self.assertTrue(data["agent_files"]["CLAUDE.md"]["is_stub"])
        self.assertTrue(data["agent_files"]["GEMINI.md"]["is_stub"])
        self.assertTrue(data["agent_files"][".cursorrules"]["is_stub"])
        self.assertFalse(data["agent_files"]["AGENTS.md"]["is_stub"])


class TestAudit(unittest.TestCase):

    def test_example_is_clean(self):
        rc, data, err = run_json("icm_audit.py", str(EXAMPLE))
        # rc=0 means clean, rc=2 means warnings exist (still acceptable for the example)
        self.assertIn(rc, (0, 2), err)
        self.assertEqual(data["summary"]["errors"], 0,
                         f"Audit errors: {data['issues']}")

    def test_audit_flags_missing_context(self):
        # Build a broken workspace in a temp dir
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "AGENTS.md").write_text("# fake\n\n## Routing\n\n| Task | Go to | Read | Skills |\n|---|---|---|---|\n", encoding="utf-8")
            (tmp / "stages" / "01-broken").mkdir(parents=True)
            # no CONTEXT.md inside the stage
            rc, data, err = run_json("icm_audit.py", str(tmp))
            self.assertEqual(rc, 2, err)
            codes = [i["code"] for i in data["issues"]]
            self.assertIn("stage_missing_context", codes)


class TestScaffold(unittest.TestCase):

    def test_scaffold_pipeline_to_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            rc, data, err = run_json(
                "icm_scaffold.py", "--template", "pipeline", "--target", str(target),
            )
            self.assertEqual(rc, 0, err)
            self.assertGreater(data["count"], 10)
            self.assertTrue((target / "AGENTS.md").exists())
            self.assertTrue((target / "stages" / "01-research" / "CONTEXT.md").exists())

    def test_scaffold_refuses_nonempty_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            target.mkdir()
            (target / "existing.txt").write_text("not empty", encoding="utf-8")
            rc, _, err = run_script(
                "icm_scaffold.py", "--template", "pipeline", "--target", str(target),
            )
            self.assertEqual(rc, 2, err)

    def test_scaffold_workspaces_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            rc, data, err = run_json(
                "icm_scaffold.py", "--template", "workspaces", "--target", str(target),
            )
            self.assertEqual(rc, 0, err)
            self.assertTrue((target / "script-lab" / "CONTEXT.md").exists())
            self.assertTrue((target / "production" / "CONTEXT.md").exists())
            self.assertTrue((target / "distribution" / "CONTEXT.md").exists())


class TestRemap(unittest.TestCase):

    def test_remap_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            run_script("icm_scaffold.py", "--template", "pipeline", "--target", str(target))
            before = (target / "AGENTS.md").read_text(encoding="utf-8")
            rc, data, err = run_json("icm_remap.py", str(target))
            self.assertEqual(rc, 0, err)
            self.assertFalse(data["wrote"])
            after = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(before, after, "Dry run should not modify the file")

    def test_remap_write_updates_routing_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            run_script("icm_scaffold.py", "--template", "pipeline", "--target", str(target))
            # Add a new stage
            new_stage = target / "stages" / "04-distribution"
            (new_stage / "references").mkdir(parents=True)
            (new_stage / "output").mkdir(parents=True)
            (new_stage / "CONTEXT.md").write_text("# Stage 04 — Distribution\n\nTest stage.\n", encoding="utf-8")
            # Remap with write
            rc, data, err = run_json("icm_remap.py", str(target), "--write")
            self.assertEqual(rc, 0, err)
            self.assertTrue(data["wrote"])
            new_text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("04-distribution", new_text)

    def test_remap_preserves_meta_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            run_script("icm_scaffold.py", "--template", "pipeline", "--target", str(target))
            # Pipeline template has a meta row "Methodology question | (here)"
            run_script("icm_remap.py", str(target), "--write")
            text = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("Methodology question", text,
                          "Meta rows with go_to=(here) should survive remap")


class TestDebloat(unittest.TestCase):

    def test_debloat_clean_example_has_no_proposals(self):
        rc, data, err = run_json("icm_debloat.py", str(EXAMPLE))
        # The example has one real research output file → clean.
        self.assertIn(rc, (0, 2), err)
        # The example might have an oversized context (review-only); should not have archive proposals.
        archive_proposals = [p for p in data["proposals"] if p["action"] == "archive"]
        self.assertEqual(len(archive_proposals), 0,
                         f"Clean example should not propose archives: {archive_proposals}")

    def test_debloat_flags_stale_empty_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            run_script("icm_scaffold.py", "--template", "pipeline", "--target", str(target))
            stale = target / "stages" / "01-research" / "output" / "old.md"
            stale.write_text("x", encoding="utf-8")
            old_time = stale.stat().st_mtime - (60 * 86400)  # 60 days ago
            os.utime(stale, (old_time, old_time))
            rc, data, _ = run_json("icm_debloat.py", str(target))
            self.assertEqual(rc, 2)
            categories = [p["category"] for p in data["proposals"]]
            self.assertIn("abandoned_output", categories)


class TestRegisterTool(unittest.TestCase):

    def test_register_tool_creates_skill_and_wires_routing(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ws"
            run_script("icm_scaffold.py", "--template", "pipeline", "--target", str(target))
            rc, data, err = run_json(
                "icm_register_tool.py",
                "--workspace", str(target),
                "--tool-name", "web-search",
                "--tool-description", "Search the web for sources during research",
                "--wire-into", "research",
            )
            self.assertEqual(rc, 0, err)
            self.assertTrue(data["wired_into_routing"])
            skill_path = Path(data["skill_path"])
            self.assertTrue(skill_path.exists())
            self.assertIn("web-search", skill_path.read_text(encoding="utf-8"))
            # Routing table should now mention the tool
            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("web-search", agents)


class TestLibInternals(unittest.TestCase):
    """Direct unit tests for _lib helpers."""

    def test_parse_render_roundtrip(self):
        sys.path.insert(0, str(SCRIPTS))
        from _lib import parse_routing_table, render_routing_table, RoutingRow
        text = """
## Routing

| Task | Go to | Read | Skills |
|------|-------|------|--------|
| A | foo/ | CONTEXT.md | — |
| B | bar/ | CONTEXT.md | skill1 |
"""
        rows = parse_routing_table(text)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].task, "A")
        self.assertEqual(rows[1].skills, "skill1")
        rendered = render_routing_table(rows)
        rows2 = parse_routing_table("## Routing\n\n" + rendered)
        self.assertEqual(rows, rows2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
