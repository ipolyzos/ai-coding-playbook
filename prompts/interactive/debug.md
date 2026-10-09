# Diagnose and fix a defect

## Inputs
- Symptoms: [observed behavior]
- Expected behavior: [contract]
- Reproduction: [commands and environment]
- Scope: [affected component]

## Workflow
1. Reproduce or explicitly document why reproduction is unavailable.
2. Form competing hypotheses grounded in logs and code.
3. Identify root cause; do not confuse correlation with causation.
4. Add a regression test that fails before the fix where feasible.
5. Apply the smallest fix, rerun tests, and report evidence and remaining uncertainty.

Do not modify unrelated code or suppress failing tests to achieve a green result.
