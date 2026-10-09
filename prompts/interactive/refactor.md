# Refactor while preserving behavior

## Inputs
- Target: [modules or paths]
- Motivation: [maintainability issue]
- Behavioral invariants: [public contracts]
- Out-of-scope changes: [exclusions]

## Workflow
1. Establish current behavior and relevant regression coverage.
2. Identify the smallest structural improvement.
3. Make incremental changes without changing external behavior.
4. Run focused and broader tests; compare public contracts where applicable.
5. Explain improvements, evidence of preserved behavior, and remaining risks.

Do not combine unrelated features or migrations with the refactor.
