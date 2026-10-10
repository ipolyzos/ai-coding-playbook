import json
from pathlib import Path
import tempfile
import unittest

from aicp.tasks import create_task


class TaskCreationTests(unittest.TestCase):
    def test_creates_contract_shape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = create_task(root, "fix-retry", "Fix retry behavior", ["src/", "tests/"], ["Relevant tests pass"])
            task = json.loads(path.read_text())
            self.assertEqual(task["objective"], "Fix retry behavior")
            self.assertEqual(task["scope"]["allowed_paths"], ["src/", "tests/"])
            self.assertIn("merge pull request", task["approval_required"])

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            create_task(root, "task", "Do work", ["src/"], ["Pass"])
            with self.assertRaises(FileExistsError):
                create_task(root, "task", "Do work", ["src/"], ["Pass"])

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                create_task(Path(temp), "task", "Do work", ["../secret"], ["Pass"])

    def test_rejects_invalid_name(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                create_task(Path(temp), "../task", "Do work", ["src"], ["Pass"])


if __name__ == "__main__":
    unittest.main()
