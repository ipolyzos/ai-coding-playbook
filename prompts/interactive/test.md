# Design and implement tests

## Inputs
- Behavior under test: [contract]
- Relevant code and test framework: [paths]
- Failure modes: [edge cases]

## Workflow
1. Inspect existing tests and behavior; identify uncovered risks.
2. Prioritize meaningful boundary, negative, and regression cases.
3. Prefer deterministic isolated tests; use integration or E2E tests for cross-boundary behavior.
4. Run focused tests and record exact commands and outcomes.
5. Report coverage limitations and tests not executed.

Do not assert coverage percentages without measuring them or weaken production behavior solely to satisfy tests.
