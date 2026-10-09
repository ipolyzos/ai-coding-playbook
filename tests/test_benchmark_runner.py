"""Benchmark runner evidence and failure behavior."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.run_benchmark import execute


class BenchmarkRunnerTests(unittest.TestCase):
    def run_case(self, command, timeout=5):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "evidence.json"
            evidence = execute({"id": "test", "command": command, "timeout_seconds": timeout}, root, output)
            self.assertEqual(evidence, json.loads(output.read_text()))
            return evidence

    def test_success(self):
        result = self.run_case([sys.executable, "-c", "print('ok')"])
        self.assertTrue(result["passed"])
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["status"], "completed")
        self.assertNotIn("stdout", result)

    def test_failure(self):
        result = self.run_case([sys.executable, "-c", "raise SystemExit(7)"])
        self.assertFalse(result["passed"])
        self.assertEqual(result["exit_code"], 7)

    def test_timeout(self):
        result = self.run_case([sys.executable, "-c", "import time; time.sleep(2)"], timeout=1)
        self.assertFalse(result["passed"])
        self.assertEqual(result["status"], "timeout")

    def test_missing_executable(self):
        result = self.run_case(["__playbook_nonexistent_executable__"])
        self.assertFalse(result["passed"])
        self.assertEqual(result["status"], "launch_error")

    def test_rejects_shell_string(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                execute({"id": "test", "command": "echo hi", "timeout_seconds": 5}, Path(directory), Path(directory) / "evidence.json")

    def test_rejects_unbounded_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                execute({"id": "test", "command": ["true"], "timeout_seconds": 9999}, Path(directory), Path(directory) / "evidence.json")


if __name__ == "__main__":
    unittest.main()
