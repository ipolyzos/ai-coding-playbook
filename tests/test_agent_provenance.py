"""Declared agent-run provenance and workspace fingerprint tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.record_agent_run import fingerprint, record


class AgentProvenanceTests(unittest.TestCase):
    def test_record_and_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "solution.py").write_text("print('ok')\n")
            transcript = root / "transcript.txt"
            transcript.write_text("agent run trace")
            output = root / "record.json"
            result = record("codex", "example", "task", workspace, transcript, output)
            self.assertEqual(result, json.loads(output.read_text()))
            self.assertEqual(result["identity_verification"], "self-declared")
            self.assertFalse(result["execution_verified"])
            self.assertEqual(result["transcript_sha256"], hashlib.sha256(b"agent run trace").hexdigest())
            self.assertNotIn("agent run trace", output.read_text())

    def test_fingerprint_changes_with_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / "file.txt"
            file.write_text("a")
            first, _ = fingerprint(root)
            file.write_text("b")
            second, _ = fingerprint(root)
            self.assertNotEqual(first, second)

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "link").symlink_to(root / "missing")
            with self.assertRaises(ValueError):
                fingerprint(root)


if __name__ == "__main__":
    unittest.main()
