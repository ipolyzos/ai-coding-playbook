# Playbook evaluations

Evaluations measure whether a workflow follows engineering constraints, not whether its prose sounds convincing. This initial harness scores **recorded outcomes** against deterministic rubrics; it does not run coding agents or verify that claims in a submitted report are truthful.

For command-execution evidence (not agent execution), see [Executable benchmarks](benchmarks/README.md).

## Run locally

```sh
python3 scripts/evaluate.py evaluations/fixtures/good-run.json
python3 -m unittest discover -s tests -v
```

## How scoring works

Each scenario defines weighted criteria. A run report supplies one `passed`, `failed`, or `not_run` outcome for every criterion. The harness validates IDs, rejects duplicates, computes the weighted pass fraction, and fails if mandatory criteria are not passed. Missing checks and unknown criteria are rejected rather than silently ignored.

A scenario passes only when all mandatory criteria pass **and** its minimum weighted score is met. Scoring a report is not a substitute for independently executing tests or reviewing the produced diff.

| Scenario | Purpose |
| --- | --- |
| [Bounded feature](scenarios/bounded-feature.json) | Scope, tests, and completion evidence |
| [Defect repair](scenarios/defect-repair.json) | Reproduction, regression test, and root cause |

## Add a scenario

Create a JSON scenario with a unique ID, weighted criteria, and a threshold in `[0, 1]`. Register the scenario in the test fixtures or use it with `--scenario`. Never label synthetic fixture results as real agent performance.

For coding-task submissions with externally provided workspaces and independent acceptance checks, see [Agent task protocol](agent-tasks/README.md). This does not yet execute or identify agents.
