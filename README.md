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
| Evaluate workflow outcomes | [Evaluation guide](evaluations/README.md) |
| Record command execution evidence | [Executable benchmarks](evaluations/benchmarks/README.md) |
| Review container execution boundaries | [Container security guide](evaluations/benchmarks/CONTAINER_SECURITY.md) |
| Verify a coding-task submission | [Agent task protocol](evaluations/agent-tasks/README.md) |
| Record agent run metadata | [Provenance protocol](evaluations/agent-tasks/PROVENANCE.md) |
| Launch an agent CLI experimentally | [CLI adapter safety guide](evaluations/agent-tasks/CLI_ADAPTER.md) |
| Contribute | [Contribution guide](CONTRIBUTING.md) |

## Quick setup\n\nUse the dependency-free CLI from a playbook checkout to initialize a separate project:\n\n\`\`\`sh\npython3 -m aicp init --tool codex --path /path/to/project\npython3 -m aicp validate --path /path/to/project\npython3 -m aicp task create --path /path/to/project --name fix-retry --objective 'Fix retry handling' --allow src/ --accept 'Unit tests pass'\n\`\`\`\n\nSee [tool-specific generated instructions](docs/TOOL_ENTRYPOINTS.md), [CLI usage and limitations](docs/CLI.md) and [local verification](docs/VERIFICATION.md). Initialization does not run an agent or install a vendor CLI.\n\n## How to use

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
- `evaluations/` — scenarios, fixtures, and scoring rubrics.
- `scripts/` — deterministic validation.
- `.github/workflows/` — CI quality gates.

## Local checks

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/validate_contracts.py
python3 -m unittest discover -s tests -v
python3 scripts/evaluate.py evaluations/fixtures/good-run.json
```

This is an incremental foundation, not the complete catalog. Additional templates and evaluation fixtures will be delivered in separate focused PRs.
