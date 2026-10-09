# AI Coding Playbook

Portable, engineering-first prompts and execution contracts for interactive AI coding and autonomous engineering workflows.

## Start here

| I want to… | Open |
| --- | --- |
| Implement a feature | [Implementation prompt](prompts/interactive/implement.md) |
| Debug a defect | [Debugging prompt](prompts/interactive/debug.md) |
| Delegate an agent task | [Task intake](prompts/autonomous/task-intake.md) |
| Validate agent work | [Validation loop](prompts/autonomous/validation-loop.md) |
| Browse all prompts | [Prompt catalog](prompts/README.md) |
| Set engineering expectations | [Engineering standards](instructions/engineering.md) |
| Require evidence | [Verification standards](instructions/verification.md) |
| Define and validate contracts | [Contract guide](contracts/README.md) |
| Configure my coding assistant | [Tool adapters](adapters/README.md) |
| Contribute | [Contribution guide](CONTRIBUTING.md) |

## How to use

1. Pick the smallest prompt matching the engineering task.
2. Supply concrete context, allowed scope, non-goals, and acceptance criteria.
3. Apply repository-specific standards alongside the shared instructions.
4. For autonomous work, use a validated task contract and explicit approval boundaries.
5. Verify changes with repository tests and CI before accepting completion.

### Example

Use [the task example](contracts/examples/feature-task.json) as a starting point for structured delegation.

## Layout

- `prompts/interactive/` — engineer-directed workflows.
- `prompts/autonomous/` — bounded agent execution workflows.
- `instructions/` — reusable engineering expectations.
- `contracts/` — machine-readable task schemas and examples.
- `adapters/` — installation guides for supported coding assistants.
- `scripts/` — deterministic validation.
- `.github/workflows/` — CI quality gates.

## Local checks

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/validate_contracts.py
python3 -m unittest discover -s tests -v
```

This is an incremental foundation, not the complete catalog. Additional templates and evaluation fixtures will be delivered in separate focused PRs.
