import json
from pathlib import Path
import tempfile
import unittest

from aicp.__main__ import main, validate_config
from aicp.adoption import adopt, plan_adoption


class AdoptionTests(unittest.TestCase):
    def test_preserves_existing_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "AGENTS.md").write_text("project-specific policy\n")
            self.assertEqual(main(["adopt", "--tool", "codex", "--path", temp, "--dry-run"]), 0)
            self.assertFalse((root / ".aicp.json").exists())
            self.assertEqual(main(["adopt", "--tool", "codex", "--path", temp]), 0)
            self.assertEqual((root / "AGENTS.md").read_text(), "project-specific policy\n")
            self.assertEqual(validate_config(root)["mode"], "adopt")
            self.assertEqual(json.loads((root / ".aicp.json").read_text())["instructions"], ".aicp/PLAYBOOK.md")

    def test_rejects_missing_existing_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                plan_adoption(Path(temp), "codex")

    def test_rejects_existing_config(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "CLAUDE.md").write_text("existing")
            (root / ".aicp.json").write_text("keep")
            with self.assertRaises(FileExistsError):
                adopt(root, "claude")
            self.assertEqual((root / ".aicp.json").read_text(), "keep")
            self.assertFalse((root / ".aicp").exists())

    def test_blocks_symlinked_sidecar_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "GEMINI.md").write_text("existing")
            (root / ".aicp").symlink_to(root, target_is_directory=True)
            self.assertFalse(plan_adoption(root, "gemini")["ready"])


if __name__ == "__main__":
    unittest.main()
