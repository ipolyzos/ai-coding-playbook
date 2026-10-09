"""Test task-manifest validation without requiring Docker."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.verify_agent_submission import verify


class SubmissionVerificationTests(unittest.TestCase):
    def test_invokes_independent_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            definition = {"id": "task", "image": "python:3.12-alpine", "acceptance": {"command": ["python3", "solution.py"], "expected_files": {"result.txt": hashlib.sha256(b"ok").hexdigest()}}}
            with patch("scripts.verify_agent_submission.run", return_value={"passed": True, "benchmark": "task"}) as runner:
                result = verify(definition, directory, directory / "evidence.json")
            self.assertTrue(result["passed"])
            self.assertEqual(result["agent_identity"], "unverified")
            self.assertEqual(runner.call_args.args[0]["command"], ["python3", "solution.py"])

    def test_missing_acceptance_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                verify({"id": "task", "image": "python:3.12-alpine"}, Path(tmp), Path(tmp) / "out.json")

    def test_missing_submission_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                verify({"id": "task", "image": "python:3.12-alpine", "acceptance": {"command": ["true"], "expected_files": {"x": "0" * 64}}}, Path(tmp) / "missing", Path(tmp) / "out.json")


if __name__ == "__main__":
    unittest.main()
