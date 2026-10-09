"""Fixture copy and independent artifact assertion tests."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.run_fixture import run_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evaluations/benchmarks/fixtures/copy-task"


class FixtureRunnerTests(unittest.TestCase):
    def test_pass_and_source_unchanged(self):
        expected = hashlib.sha256(b"ENGINEERING EVIDENCE\n").hexdigest()
        definition = {"id": "copy-task", "command": ["python3", "solution.py"], "timeout_seconds": 10, "expected_files": {"result.txt": expected}}
        with tempfile.TemporaryDirectory() as tmp:
            result = run_fixture(definition, FIXTURE, Path(tmp) / "evidence.json")
            self.assertTrue(result["passed"])
            self.assertTrue(result["assertions"]["result.txt"])
            self.assertFalse((FIXTURE / "result.txt").exists())

    def test_wrong_digest_fails(self):
        definition = {"id": "copy-task", "command": ["python3", "solution.py"], "timeout_seconds": 10, "expected_files": {"result.txt": "0" * 64}}
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(run_fixture(definition, FIXTURE, Path(tmp) / "evidence.json")["passed"])

    def test_parent_traversal_rejected(self):
        definition = {"id": "bad", "command": ["python3", "solution.py"], "timeout_seconds": 10, "expected_files": {"../outside": "0" * 64}}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                run_fixture(definition, FIXTURE, Path(tmp) / "evidence.json")


if __name__ == "__main__":
    unittest.main()
