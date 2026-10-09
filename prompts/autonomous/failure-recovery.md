# Failure recovery

## Objective
Recover safely from failing tests, interrupted commands, or partial changes.

## Workflow
1. Capture the failing command, exit code, environment, and relevant output.
2. Classify the failure as attributable, pre-existing, or unknown based on evidence.
3. Retry only bounded, reversible remediation within approved scope.
4. After three unsuccessful remediation attempts, stop and report; never hide failures or bypass quality gates.

## Required output
Report evidence, unresolved questions, checks performed, and any approval required before proceeding.
