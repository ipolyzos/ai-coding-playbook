"""Supervised execution orchestration tests; no real agent is launched."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from aicp.execution import run_task
from aicp.tasks import create_task


class RunTaskTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        create_task(self.project, "fix-retry", "Fix retry", ["src/"], ["Tests pass"])
        self.checks = self.project / "checks.json"
        self.checks.write_text('{"schema_version":1,"checks":[["python3","--version"]]}', encoding="utf-8")
        self.output = self.project / "report.json"

    def test_successful_agent_and_checks(self):
        with patch("aicp.execution.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = b"ok"
            run.return_value.stderr = b""
            result = run_task(self.project, "fix-retry", "codex", ["codex", "exec", "example"], self.checks, self.output)
        self.assertTrue(result["passed"])
        self.assertFalse(result["scope_enforced"])
        self.assertEqual(json.loads(self.output.read_text(encoding="utf-8"))["task"], "fix-retry")

    def test_agent_failure_skips_checks(self):
        with patch("aicp.execution.subprocess.run") as run:
            run.return_value.returncode = 1
            run.return_value.stdout = b""
            run.return_value.stderr = b"error"
            result = run_task(self.project, "fix-retry", "codex", ["codex", "exec", "example"], self.checks, self.output)
        self.assertFalse(result["passed"])
        self.assertIsNone(result["verification"])

    def test_agent_modified_checks_are_rejected_without_running_them(self):
        def tamper(*args, **kwargs):
            self.checks.write_text('{"schema_version":1,"checks":[["python3","-c","print(123)"]]}', encoding="utf-8")
            return type("Completed", (), {"returncode": 0, "stdout": b"", "stderr": b""})()

        with patch("aicp.execution.subprocess.run", side_effect=tamper):
            with patch("aicp.execution.run_checks") as checks:
                result = run_task(self.project, "fix-retry", "codex", ["codex"], self.checks, self.output)
        checks.assert_not_called()
        self.assertFalse(result["passed"])
        self.assertFalse(result["trusted_inputs"]["unchanged_after_agent"])
        self.assertIsNone(result["verification"])

    def test_agent_modified_task_is_rejected(self):
        def tamper(*args, **kwargs):
            task = self.project / "tasks" / "fix-retry.json"
            task.write_text(task.read_text(encoding="utf-8") + " ", encoding="utf-8")
            return type("Completed", (), {"returncode": 0, "stdout": b"", "stderr": b""})()

        with patch("aicp.execution.subprocess.run", side_effect=tamper):
            result = run_task(self.project, "fix-retry", "codex", ["codex"], self.checks, self.output)
        self.assertFalse(result["passed"])
        self.assertFalse(result["trusted_inputs"]["unchanged_after_agent"])

    def test_invalid_checks_fail_before_agent_execution(self):
        self.checks.write_text('{"schema_version":1,"checks":[]}', encoding="utf-8")
        with patch("aicp.execution.subprocess.run") as agent:
            with self.assertRaises(ValueError):
                run_task(self.project, "fix-retry", "codex", ["codex"], self.checks, self.output)
        agent.assert_not_called()

    def test_invalid_agent_command_rejected(self):
        with self.assertRaises(ValueError):
            run_task(self.project, "fix-retry", "codex", ["sh", "-c", "true"], self.checks, self.output)

    def test_report_never_overwritten(self):
        self.output.write_text("existing", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            run_task(self.project, "fix-retry", "codex", ["codex"], self.checks, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "existing")


if __name__ == "__main__":
    unittest.main()
