import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import subprocess

from aicp.verification import run_checks, verify


class VerificationTests(unittest.TestCase):
    def test_pass_and_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = run_checks(root, [[sys.executable, "-c", "print('ok')"], [sys.executable, "-c", "raise SystemExit(2)"]])
            self.assertFalse(result["passed"])
            self.assertEqual([x["passed"] for x in result["checks"]], [True, False])
            self.assertEqual(result["checks"][1]["exit_code"], 2)

    def test_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch("aicp.verification.subprocess.run", side_effect=subprocess.TimeoutExpired(["test"], 1)):
                result = run_checks(Path(temp), [["test"]])
            self.assertEqual(result["checks"][0]["status"], "timeout")
            self.assertFalse(result["passed"])

    def test_config(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "checks.json").write_text(json.dumps({"schema_version": 1, "checks": [[sys.executable, "-c", "pass"]]}))
            self.assertTrue(verify(root, root / "checks.json")["passed"])

    def test_rejects_empty_checks(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                run_checks(Path(temp), [])


if __name__ == "__main__":
    unittest.main()
