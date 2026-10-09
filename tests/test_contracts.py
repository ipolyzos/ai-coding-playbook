"""Contract regression tests."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


class ContractTests(unittest.TestCase):
    def test_all_examples_validate(self):
        from scripts.validate_contracts import validate_examples
        validate_examples()

    def test_task_rejects_missing_scope(self):
        schema = json.loads((CONTRACTS / "task.schema.json").read_text())
        instance = json.loads((CONTRACTS / "examples/feature-task.json").read_text())
        del instance["scope"]
        self.assertFalse(Draft202012Validator(schema).is_valid(instance))

    def test_validation_rejects_unknown_status(self):
        schema = json.loads((CONTRACTS / "validation.schema.json").read_text())
        instance = json.loads((CONTRACTS / "examples/validation-report.json").read_text())
        instance["checks"][0]["status"] = "probably_passed"
        self.assertFalse(Draft202012Validator(schema).is_valid(instance))

    def test_completion_rejects_missing_evidence_status(self):
        schema = json.loads((CONTRACTS / "completion.schema.json").read_text())
        instance = json.loads((CONTRACTS / "examples/completion-report.json").read_text())
        del instance["acceptance"][0]["status"]
        self.assertFalse(Draft202012Validator(schema).is_valid(instance))


if __name__ == "__main__":
    unittest.main()
