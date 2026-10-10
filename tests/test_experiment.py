"""Experimental manifest validation tests."""
import unittest
from aicp.experiment import validate_manifest


class ExperimentManifestTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "schema_version": 1,
            "experiment_id": "pilot",
            "agent": "codex-version",
            "fixture_revision": "abc123",
            "tasks": ["bug-fix", "test-addition"],
            "repetitions": 3,
            "timeout_seconds": 900,
        }

    def test_valid(self):
        self.assertEqual(validate_manifest(self.manifest), self.manifest)

    def test_duplicate_tasks(self):
        self.manifest["tasks"].append("bug-fix")
        with self.assertRaises(ValueError):
            validate_manifest(self.manifest)

    def test_invalid_repetitions(self):
        self.manifest["repetitions"] = True
        with self.assertRaises(ValueError):
            validate_manifest(self.manifest)

    def test_unexpected_fields(self):
        self.manifest["result"] = "pass"
        with self.assertRaises(ValueError):
            validate_manifest(self.manifest)


if __name__ == "__main__":
    unittest.main()
