"""Synthetic task fixture isolation and validity tests."""
from pathlib import Path
import tempfile
import unittest

from aicp.synthetic_fixtures import TASKS, materialize_fixture


class SyntheticFixtureTests(unittest.TestCase):
    def test_five_distinct_tasks_materialize(self):
        self.assertEqual(set(TASKS), {"bug-fix", "test-addition", "refactoring", "documentation", "feature"})
        for name in TASKS:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                workspace, evaluator = root / "workspace", root / "evaluator"
                materialize_fixture(name, workspace, evaluator)
                self.assertTrue((workspace / "app.py").is_file())
                self.assertTrue((workspace / "TASK.md").is_file())
                self.assertTrue((evaluator / "acceptance.py").is_file())
                self.assertFalse((workspace / "acceptance.py").exists())
                compile((workspace / "app.py").read_text(encoding="utf-8"), "app.py", "exec")
                compile((evaluator / "acceptance.py").read_text(encoding="utf-8"), "acceptance.py", "exec")

    def test_never_overwrites_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workspace").mkdir()
            with self.assertRaises(ValueError):
                materialize_fixture("bug-fix", root / "workspace", root / "evaluator")

    def test_unknown_task_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaises(ValueError):
                materialize_fixture("unknown", root / "workspace", root / "evaluator")


if __name__ == "__main__":
    unittest.main()
