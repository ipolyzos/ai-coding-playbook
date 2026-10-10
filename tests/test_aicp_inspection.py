import json
from pathlib import Path
import tempfile
import unittest

from aicp.inspection import inspect_project
from aicp.__main__ import main


class InspectionTests(unittest.TestCase):
    def test_empty_repo_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = inspect_project(project)
            self.assertFalse(result["requires_manual_review"])
            self.assertEqual(list(project.iterdir()), [])

    def test_existing_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "AGENTS.md").write_text("custom policy")
            result = inspect_project(project)
            self.assertTrue(result["requires_manual_review"])
            self.assertIn("AGENTS.md", result["existing_instructions"])
            self.assertEqual((project / "AGENTS.md").read_text(), "custom policy")

    def test_symlink_detected_without_following(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / ".cursor").symlink_to(project, target_is_directory=True)
            result = inspect_project(project)
            cursor = next(item for item in result["files"] if item["path"].startswith(".cursor/"))
            self.assertEqual(cursor["status"], "unsafe")

    def test_cli_json(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(main(["inspect", "--path", temp]), 0)


if __name__ == "__main__":
    unittest.main()
