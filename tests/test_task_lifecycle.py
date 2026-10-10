"""Task lifecycle command regressions."""
import json
from pathlib import Path
import tempfile
import unittest

from aicp.task_lifecycle import list_tasks, show_task, validate_task_data
from aicp.tasks import create_task


class TaskLifecycleTests(unittest.TestCase):
    def test_create_show_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_task(root, "fix-retry", "Fix retry", ["src/", "tests/"], ["Tests pass"])
            self.assertEqual(list_tasks(root), ["fix-retry"])
            self.assertEqual(show_task(root, "fix-retry")["objective"], "Fix retry")

    def test_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(list_tasks(Path(tmp)), [])

    def test_invalid_task_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tasks").mkdir()
            (root / "tasks" / "broken.json").write_text('{"objective":"x"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                show_task(root, "broken")
            with self.assertRaises(ValueError):
                list_tasks(root)

    def test_symlinked_task_directory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "outside").mkdir()
            (root / "project").mkdir()
            (root / "project" / "tasks").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(ValueError):
                list_tasks(root / "project")

    def test_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                show_task(Path(tmp), "../secret")

    def test_contract_rejects_extra_fields(self):
        with self.assertRaises(ValueError):
            validate_task_data({"objective": "test", "unexpected": True})


if __name__ == "__main__":
    unittest.main()
