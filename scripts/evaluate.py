#!/usr/bin/env python3
"""Deterministically score recorded evaluation outcomes; does not execute agents."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "evaluations" / "scenarios"


def score(scenario, report):
    if report.get("scenario") != scenario.get("id"):
        raise ValueError("Scenario ID mismatch")
    criteria = scenario.get("criteria", [])
    ids = [item["id"] for item in criteria]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Scenario criteria must be nonempty and unique")
    threshold = scenario.get("minimum_score")
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not 0 <= threshold <= 1:
        raise ValueError("minimum_score must be between 0 and 1")
    weights = [item["weight"] for item in criteria]
    if any(not isinstance(w, (int, float)) or isinstance(w, bool) or w <= 0 for w in weights):
        raise ValueError("All weights must be positive")
    outcomes = report.get("outcomes", [])
    observed = [item["criterion"] for item in outcomes]
    if len(observed) != len(set(observed)) or set(observed) != set(ids):
        raise ValueError("Outcomes must match each criterion exactly once")
    statuses = {item["criterion"]: item["status"] for item in outcomes}
    if set(statuses.values()) - {"passed", "failed", "not_run"}:
        raise ValueError("Invalid outcome status")
    total = sum(weights)
    value = sum(item["weight"] for item in criteria if statuses[item["id"]] == "passed") / total
    mandatory_ok = all(statuses[item["id"]] == "passed" for item in criteria if item.get("mandatory", False))
    return {"scenario": scenario["id"], "score": round(value, 4), "mandatory_passed": mandatory_ok, "passed": mandatory_ok and value >= threshold}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--scenario", type=Path, help="Override scenario file")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    path = args.scenario or SCENARIOS / (report["scenario"] + ".json")
    scenario = json.loads(path.read_text(encoding="utf-8"))
    result = score(scenario, report)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
