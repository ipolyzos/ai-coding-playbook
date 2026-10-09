#!/usr/bin/env python3
"""Validate contract schemas and example instances using Draft 2020-12."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
EXAMPLES = CONTRACTS / "examples"
MAPPINGS = {
    "feature-task.json": "task.schema.json",
    "validation-report.json": "validation.schema.json",
    "completion-report.json": "completion.schema.json",
}


def validate_examples():
    for schema_file in sorted(CONTRACTS.glob("*.schema.json")):
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    for example, schema_file in MAPPINGS.items():
        instance = json.loads((EXAMPLES / example).read_text(encoding="utf-8"))
        schema = json.loads((CONTRACTS / schema_file).read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(map(str, e.path)))
        if errors:
            raise ValueError(f"{example}: " + "; ".join(error.message for error in errors))
    unregistered = {p.name for p in EXAMPLES.glob("*.json")} - set(MAPPINGS)
    if unregistered:
        raise ValueError(f"Unregistered contract examples: {sorted(unregistered)}")


if __name__ == "__main__":
    validate_examples()
    print("Contract schemas and examples validated")
