from pathlib import Path
import tempfile
import unittest

from aicp.planning import plan_init


class InitPlanningTests(unittest.TestCase):
    def test_preview_has_no_side_effects(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            plan = plan_init(project, "claude")
            self.assertTrue(plan["ready"])
            self.assertEqual([f["path"] for f in plan["files"]], [".aicp.json", "AGENTS.md", "CLAUDE.md"])
            self.assertEqual(list(project.iterdir()), [])

    def test_existing_file_blocks_preview(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "AGENTS.md").write_text("existing")
            plan = plan_init(project, "codex")
            self.assertFalse(plan["ready"])
            self.assertEqual(plan["files"][1]["action"], "blocked")
            self.assertEqual((project / "AGENTS.md").read_text(), "existing")

    def test_symlink_parent_blocks_preview(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / ".cursor").symlink_to(project, target_is_directory=True)
            plan = plan_init(project, "cursor")
            self.assertFalse(plan["ready"])


if __name__ == "__main__":
    unittest.main()
