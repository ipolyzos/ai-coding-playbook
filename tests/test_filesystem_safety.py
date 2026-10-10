"""Regression tests for conservative path checks."""
from pathlib import Path
import tempfile
import unittest

from aicp.__main__ import init, validate_config
from aicp.tasks import create_task


class FilesystemSafetyTests(unittest.TestCase):
    def test_task_rejects_symlinked_tasks_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            outside = root / "outside"
            project.mkdir()
            outside.mkdir()
            (project / "tasks").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                create_task(project, "fix-retry", "Fix retry", ["src/"], ["Tests pass"])
            self.assertEqual(list(outside.iterdir()), [])

    def test_task_rejects_file_as_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "tasks").write_text("occupied", encoding="utf-8")
            with self.assertRaises(ValueError):
                create_task(project, "fix-retry", "Fix retry", ["src/"], ["Tests pass"])

    def test_validate_rejects_symlinked_adoption_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            outside = root / "outside"
            project.mkdir()
            outside.mkdir()
            (project / "AGENTS.md").write_text("# existing", encoding="utf-8")
            (outside / "PLAYBOOK.md").write_text("# AI Coding Playbook", encoding="utf-8")
            (project / ".aicp").symlink_to(outside, target_is_directory=True)
            (project / ".aicp.json").write_text(
                '{"schema_version":1,"tool":"codex","instructions":".aicp/PLAYBOOK.md","mode":"adopt"}',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                validate_config(project)

    def test_validate_requires_tool_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            init(project, "claude")
            validate_config(project)
            (project / "CLAUDE.md").unlink()
            with self.assertRaisesRegex(ValueError, "entrypoint"):
                validate_config(project)

    def test_task_rejects_symlink_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            (root / "alias").symlink_to(project, target_is_directory=True)
            with self.assertRaises(ValueError):
                create_task(root / "alias", "fix-retry", "Fix retry", ["src/"], ["Tests pass"])


if __name__ == "__main__":
    unittest.main()
