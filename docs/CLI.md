# AICP CLI (foundation)

Run directly from a checkout of the playbook, using the Python standard library:

```sh
python3 -m aicp init --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
python3 -m aicp --version
```

Supported tool labels: `codex`, `claude`, `cursor`, `copilot`, `gemini`. Initialization creates a minimal `AGENTS.md` and `.aicp.json` in an **existing** project directory. It never overwrites either file. Validation checks configuration shape and the presence of generated instructions; it does **not** enforce tool-specific policies, execute tests, or prove adherence to engineering standards.

This is a minimal, tool-neutral onboarding step. It does not install vendor CLIs, create tasks, or run agents. Future increments can provide vendor-specific setup, `task create`, and `verify` commands.

## Create an engineering task\n\nAfter initialization:\n\n\`\`\`sh\npython3 -m aicp task create --path /path/to/project --name fix-retry --objective 'Fix consumer retry behavior' --allow src/ --allow tests/ --accept 'Unit tests pass' --accept 'Existing behavior is preserved by default'\n\`\`\`\n\nThis creates \`tasks/fix-retry.json\` with the existing task contract fields and explicit approval boundaries. It does not launch an agent or verify that the acceptance criteria are satisfied. Existing tasks are never overwritten.\n
## Preview initialization safely\n\nRun `python3 -m aicp init --tool claude --path /path/to/project --dry-run` to inspect the proposed files and conflicts before writing anything. The JSON result marks each target as `create` or `blocked` and returns a nonzero status when any target is blocked. Existing assistant instructions are never silently overwritten or merged. Review conflicts manually, preserve existing project policy, and rerun initialization only after resolving them. The normal `init` path performs the same preflight, including rejecting symlinked destination parent directories.\n
## Inspect existing instructions\n\nBefore initialization in an established repository, run `python3 -m aicp inspect --path /path/to/project`. This is a read-only inventory of known assistant instruction paths. See [inspection details](INSPECTION.md). It does not merge or alter existing policies.\n