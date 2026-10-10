"""CLI adapter unit tests; never launch actual agent binaries."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

from scripts.run_agent_cli import run_agent, validate_tool


class AgentCliTests(unittest.TestCase):
    def test_rejects_other_programs(self):
        with self.assertRaises(ValueError):
            validate_tool("sh", ["sh", "-c", "true"], 10)
        with self.assertRaises(ValueError):
            validate_tool("codex", ["python3", "-c", "print(1)"], 10)

    def test_rejects_unbounded_timeout(self):
        with self.assertRaises(ValueError):
            validate_tool("codex", ["codex"], 99999)

    def test_records_mocked_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "task.txt").write_text("initial")
            output = root / "evidence.json"
            with patch("scripts.run_agent_cli.subprocess.run", return_value=subprocess.CompletedProcess(["codex"], 0, b"ok", b"")) as proc:
                result = run_agent("codex", ["codex", "exec", "test"], "task", workspace, output, 5)
            self.assertTrue(result["passed"])
            self.assertEqual(result, json.loads(output.read_text()))
            self.assertEqual(result["identity_verification"], "executable-name-only")
            self.assertEqual(result["stdout_bytes"], 2)
            self.assertNotIn("ok", output.read_text())
            self.assertNotIn("OPENAI_API_KEY", proc.call_args.kwargs["env"])

    def test_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            with patch("scripts.run_agent_cli.subprocess.run", side_effect=subprocess.TimeoutExpired("codex", 1)):
                result = run_agent("codex", ["codex"], "task", workspace, root / "out.json", 1)
            self.assertFalse(result["passed"])
            self.assertEqual(result["status"], "timeout")


if __name__ == "__main__":
    unittest.main()
