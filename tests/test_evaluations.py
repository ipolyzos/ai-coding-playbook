"""Deterministic evaluation harness regression tests."""
import copy
import json
import unittest
from pathlib import Path

from scripts.evaluate import score

ROOT = Path(__file__).resolve().parents[1] / "evaluations"


class EvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenario = json.loads((ROOT / "scenarios/bounded-feature.json").read_text())
        cls.good = json.loads((ROOT / "fixtures/good-run.json").read_text())

    def test_good_report_passes(self):
        self.assertTrue(score(self.scenario, self.good)["passed"])

    def test_mandatory_failure_blocks(self):
        bad = json.loads((ROOT / "fixtures/failed-run.json").read_text())
        self.assertFalse(score(self.scenario, bad)["passed"])

    def test_missing_criterion_rejected(self):
        report = copy.deepcopy(self.good)
        report["outcomes"].pop()
        with self.assertRaises(ValueError):
            score(self.scenario, report)

    def test_duplicate_criterion_rejected(self):
        report = copy.deepcopy(self.good)
        report["outcomes"][1]["criterion"] = "scope"
        with self.assertRaises(ValueError):
            score(self.scenario, report)

    def test_invalid_status_rejected(self):
        report = copy.deepcopy(self.good)
        report["outcomes"][0]["status"] = "maybe"
        with self.assertRaises(ValueError):
            score(self.scenario, report)

    def test_wrong_scenario_rejected(self):
        report = copy.deepcopy(self.good)
        report["scenario"] = "different"
        with self.assertRaises(ValueError):
            score(self.scenario, report)


if __name__ == "__main__":
    unittest.main()
