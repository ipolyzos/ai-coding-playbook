# Getting started

For a complete worked example, see the [practical walkthrough](PRACTICAL_WALKTHROUGH.md).

## Quick setup

Clone the playbook, then run its dependency-free CLI from the playbook directory to initialize an existing project:

```sh
git clone https://github.com/ipolyzos/ai-coding-playbook.git
cd ai-coding-playbook
python3 -m aicp init --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
python3 -m aicp task create \
  --path /path/to/project \
  --name fix-retry \
  --objective 'Fix retry handling' \
  --allow src/ \
  --accept 'Unit tests pass'
```

Replace `/path/to/project` with the path to an existing directory. Initialization refuses to overwrite existing assistant instructions; use `python3 -m aicp init --tool codex --path /path/to/project --dry-run` to preview changes first.

See [tool-specific generated instructions](./TOOL_ENTRYPOINTS.md), [CLI usage and limitations](./CLI.md), and [local verification](./VERIFICATION.md). Initialization does not run an agent or install a vendor CLI.

For repositories that already have assistant instructions, use the [non-destructive adoption workflow](./ADOPTION.md) instead of replacing existing policy files.

## How to use

1. Pick the smallest prompt matching the engineering task.
2. Supply concrete context, allowed scope, non-goals, and acceptance criteria.
3. Apply repository-specific standards alongside the shared instructions.
4. For autonomous work, use a validated task contract and explicit approval boundaries.
5. Verify changes with repository tests and CI before accepting completion.

### Example

Use [the task example](../contracts/examples/feature-task.json) as a starting point for structured delegation.

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
