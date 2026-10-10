"""Descriptive, paired summaries for recorded experimental runs.

No statistical significance or causal claims are inferred.
"""
import json
from pathlib import Path
from statistics import mean

REQUIRED = {"task", "repetition", "condition", "passed", "duration_seconds", "human_interventions", "review_minutes", "cost_usd"}


def analyze_runs(runs):
    if not isinstance(runs, list) or not runs:
        raise ValueError("Expected nonempty experimental runs")
    pairs = {}
    for run in runs:
        if not isinstance(run, dict) or set(run) != REQUIRED:
            raise ValueError("Invalid run fields")
        if not isinstance(run["task"], str) or not run["task"].strip():
            raise ValueError("Invalid task")
        if type(run["repetition"]) is not int or run["repetition"] < 1:
            raise ValueError("Invalid repetition")
        if run["condition"] not in ("baseline", "playbook") or type(run["passed"]) is not bool:
            raise ValueError("Invalid condition or pass status")
        for key in ("duration_seconds", "human_interventions", "review_minutes", "cost_usd"):
            value = run[key]
            if value is not None and (type(value) not in (int, float) or value < 0):
                raise ValueError("Invalid metric: " + key)
        key = (run["task"], run["repetition"])
        pair = pairs.setdefault(key, {})
        if run["condition"] in pair:
            raise ValueError("Duplicate task/repetition/condition")
        pair[run["condition"]] = run

    complete = [pair for pair in pairs.values() if set(pair) == {"baseline", "playbook"}]
    if not complete:
        raise ValueError("No complete baseline/playbook pairs")
    summary = {
        "schema_version": 1,
        "complete_pairs": len(complete),
        "incomplete_pairs": len(pairs) - len(complete),
        "conditions": {},
        "paired_pass_rate_difference": mean(
            int(p["playbook"]["passed"]) - int(p["baseline"]["passed"]) for p in complete
        ),
        "limitations": "descriptive-only; paired observations are not proof of causality or statistical significance",
    }
    for condition in ("baseline", "playbook"):
        rows = [p[condition] for p in complete]
        result = {"runs": len(rows), "passed": sum(r["passed"] for r in rows), "pass_rate": mean(r["passed"] for r in rows)}
        for key in ("duration_seconds", "human_interventions", "review_minutes", "cost_usd"):
            values = [r[key] for r in rows if r[key] is not None]
            result["mean_" + key] = mean(values) if values else None
            result["observed_" + key] = len(values)
        summary["conditions"][condition] = result
    return summary


def analyze_file(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("Results file must be a regular file")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"schema_version", "runs"} or data["schema_version"] != 1:
        raise ValueError("Invalid results file")
    return analyze_runs(data["runs"])


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Summarize recorded experimental runs")
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.dumps(analyze_file(args.results), indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(report)
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
