# Experimental results analysis

**No live agent benchmark results have been collected or published by this project yet.** This analyzer reports descriptive statistics from explicitly supplied observations. It does not execute agents, measure elapsed time itself, calculate confidence intervals, or establish causality.

## Input

Prepare a JSON file containing `{"schema_version": 1, "runs": [...]}`. Each run has exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| `task` | string | Stable synthetic task identifier |
| `repetition` | positive integer | Matched run index |
| `condition` | string | `baseline` or `playbook` |
| `passed` | boolean | Independent held-out acceptance outcome |
| `duration_seconds` | nonnegative number or null | Observed elapsed time |
| `human_interventions` | nonnegative number or null | Observed intervention count |
| `review_minutes` | nonnegative number or null | Observed review effort |
| `cost_usd` | nonnegative number or null | Observed monetary cost |

Unknown telemetry must be `null`, **not zero**. Task and repetition identify a pair. The analyzer rejects duplicate observations and summarizes complete pairs only; it counts incomplete pairs separately.

## Run

```sh
python3 -m aicp.results_analysis /path/to/observations.json --output /tmp/aicp-analysis.json
```

The output contains pass rates, paired pass-rate difference (playbook minus baseline), mean observed metrics and observation counts. These are descriptive statistics; they are not a statistical significance test or proof that the playbook caused an improvement.

Follow the [experimental protocol](../../docs/EXPERIMENTAL_PROTOCOL.md) for randomized or counterbalanced experiments, independent acceptance checks, and transparent reporting of failures. Publish the exact environment, fixtures, agent/model versions, all raw outcomes, and limitations before drawing conclusions.
