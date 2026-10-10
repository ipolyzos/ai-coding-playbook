"""Verification summaries do not expose captured command output."""
import sys
import tempfile
from pathlib import Path
import unittest

from aicp.verification import run_checks


class VerificationDiagnosticsTests(unittest.TestCase):
    def test_pass_fail_and_timeout_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            checks = [
                [sys.executable, "-c", "print('ok')"],
                [sys.executable, "-c", "raise SystemExit(2)"],
                [sys.executable, "-c", "import time; time.sleep(3)"],
            ]
            result = run_checks(project, checks, timeout=1)
            self.assertFalse(result["passed"])
            self.assertEqual(result["summary"], {
                "total": 3, "passed": 1, "failed": 2,
                "timed_out": 1, "launch_errors": 0,
            })
            self.assertNotIn("stdout", result["checks"][0])
            self.assertIn("stdout_sha256", result["checks"][0])

    def test_launch_error_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_checks(Path(tmp), [["/nonexistent-aicp-executable"]])
            self.assertEqual(result["summary"]["launch_errors"], 1)


if __name__ == "__main__":
    unittest.main()
