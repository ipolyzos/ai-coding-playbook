"""Descriptive experiment results tests; data is illustrative, not measured."""
import unittest

from aicp.results_analysis import analyze_runs


def run(condition, passed, repetition=1, duration=10.0):
    return {
        "task": "bug-fix", "repetition": repetition, "condition": condition,
        "passed": passed, "duration_seconds": duration,
        "human_interventions": 0, "review_minutes": None, "cost_usd": None,
    }


class ResultsAnalysisTests(unittest.TestCase):
    def test_paired_rates_and_missing_telemetry(self):
        report = analyze_runs([
            run("baseline", False, 1, 20),
            run("playbook", True, 1, 10),
            run("baseline", True, 2, 12),
            run("playbook", True, 2, 14),
        ])
        self.assertEqual(report["complete_pairs"], 2)
        self.assertEqual(report["paired_pass_rate_difference"], 0.5)
        self.assertEqual(report["conditions"]["baseline"]["pass_rate"], 0.5)
        self.assertIsNone(report["conditions"]["playbook"]["mean_cost_usd"])
        self.assertEqual(report["conditions"]["baseline"]["observed_cost_usd"], 0)

    def test_incomplete_pairs_not_scored(self):
        report = analyze_runs([run("baseline", False), run("playbook", True), run("baseline", True, 2)])
        self.assertEqual(report["complete_pairs"], 1)
        self.assertEqual(report["incomplete_pairs"], 1)

    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):
            analyze_runs([run("baseline", True), run("baseline", False), run("playbook", True)])

    def test_missing_pairs_rejected(self):
        with self.assertRaises(ValueError):
            analyze_runs([run("baseline", True)])

    def test_negative_metric_rejected(self):
        row = run("baseline", True)
        row["cost_usd"] = -1
        with self.assertRaises(ValueError):
            analyze_runs([row, run("playbook", True)])


if __name__ == "__main__":
    unittest.main()
