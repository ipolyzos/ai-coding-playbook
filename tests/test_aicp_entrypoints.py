from pathlib import Path
import tempfile
import unittest

from aicp.__main__ import init
from aicp.entrypoints import ENTRYPOINTS


class EntrypointTests(unittest.TestCase):
    def test_init_all_tools(self):
        for tool, relative in ENTRYPOINTS.items():
            with self.subTest(tool=tool), tempfile.TemporaryDirectory() as temp:
                project = Path(temp)
                init(project, tool)
                self.assertTrue((project / "AGENTS.md").is_file())
                if relative:
                    path = project / relative
                    self.assertTrue(path.is_file())
                    self.assertIn("AGENTS.md", path.read_text())

    def test_refuses_existing_tool_file_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "CLAUDE.md").write_text("original")
            with self.assertRaises(FileExistsError):
                init(project, "claude")
            self.assertFalse((project / ".aicp.json").exists())
            self.assertFalse((project / "AGENTS.md").exists())
            self.assertEqual((project / "CLAUDE.md").read_text(), "original")


if __name__ == "__main__":
    unittest.main()
