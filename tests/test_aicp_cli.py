import json
from pathlib import Path
import tempfile
import unittest

from aicp.__main__ import init, main, validate_config


class CliTests(unittest.TestCase):
    def test_init_and_validate(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            self.assertEqual(main(["init", "--tool", "codex", "--path", str(path)]), 0)
            self.assertEqual(main(["validate", "--path", str(path)]), 0)
            self.assertEqual(validate_config(path)["tool"], "codex")
            self.assertEqual(json.loads((path / ".aicp.json").read_text())["schema_version"], 1)

    def test_never_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / "AGENTS.md").write_text("original")
            with self.assertRaises(FileExistsError):
                init(path, "claude")
            self.assertEqual((path / "AGENTS.md").read_text(), "original")

    def test_rejects_invalid_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            init(path, "cursor")
            (path / ".aicp.json").write_text('{"schema_version": 1, "tool": "other", "instructions": "AGENTS.md"}')
            self.assertEqual(main(["validate", "--path", str(path)]), 1)

    def test_rejects_missing_target(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                init(Path(temp) / "missing", "codex")


if __name__ == "__main__":
    unittest.main()
