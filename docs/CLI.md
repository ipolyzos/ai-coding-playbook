# AICP CLI (foundation)

Run directly from a checkout of the playbook, using the Python standard library:

```sh
python3 -m aicp init --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
python3 -m aicp --version
```

Supported tool labels: `codex`, `claude`, `cursor`, `copilot`, `gemini`. Initialization creates a minimal `AGENTS.md` and `.aicp.json` in an **existing** project directory. It never overwrites either file. Validation checks configuration shape and the presence of generated instructions; it does **not** enforce tool-specific policies, execute tests, or prove adherence to engineering standards.

This is a tool-neutral onboarding step. It does not install vendor CLIs or run agents. Task creation and local verification are separate explicit commands.

## Create an engineering task

After initialization:

```sh
python3 -m aicp task create --path /path/to/project --name fix-retry --objective 'Fix consumer retry behavior' --allow src/ --allow tests/ --accept 'Unit tests pass' --accept 'Existing behavior is preserved by default'
```

This creates `tasks/fix-retry.json` with the existing task contract fields and explicit approval boundaries. It does not launch an agent or verify that the acceptance criteria are satisfied. Existing tasks are never overwritten.

## Preview initialization safely

Run `python3 -m aicp init --tool claude --path /path/to/project --dry-run` to inspect the proposed files and conflicts before writing anything. The JSON result marks each target as `create` or `blocked` and returns a nonzero status when any target is blocked. Existing assistant instructions are never silently overwritten or merged. Review conflicts manually, preserve existing project policy, and rerun initialization only after resolving them. The normal `init` path performs the same preflight, including rejecting symlinked destination parent directories.

## Inspect existing instructions

Before initialization in an established repository, run `python3 -m aicp inspect --path /path/to/project`. This is a read-only inventory of known assistant instruction paths. See [inspection details](INSPECTION.md). It does not merge or alter existing policies.

## Adopt existing instructions

Use [non-destructive adoption](ADOPTION.md) when a project already has assistant instructions. The generated sidecar is not automatically loaded by assistants.

## Filesystem safety

Task creation rejects symlinked `tasks/` directories, non-directory destination parents, and symlinked project roots. `validate` checks that the configured playbook instructions have safe path ancestry and that tool-specific instruction entrypoints created by `init` still exist. These checks are conservative preflight protections, **not** atomic filesystem isolation against a concurrent attacker. Do not run the CLI in untrusted directories with concurrent modifications or elevated permissions.

## Review existing tasks

Use `python3 -m aicp task list --path /path/to/project` to list and validate local task drafts, `python3 -m aicp task show --path /path/to/project --name fix-retry` to print a task, and `python3 -m aicp task validate --path /path/to/project --name fix-retry` for a machine-readable validity result. Invalid or symlinked task files are rejected. Validation checks structure and basic allowed-path syntax; it **does not enforce agent permissions, inspect whether a task is completed, or execute acceptance criteria**.

## Supervised agent execution (experimental)

The `aicp run` command invokes an explicitly selected local Codex, Claude, or Gemini CLI and, **only after a successful agent exit**, runs trusted checks. It requires `--approve-host-execution`. Example, in a disposable isolated environment with the vendor CLI already installed and authenticated:

```sh
aicp run --path /path/to/project --name fix-retry \
  --tool codex --checks /path/to/project/checks.json \
  --output /tmp/aicp-run.json --approve-host-execution \
  -- codex exec "Read tasks/fix-retry.json and implement the approved task"
```

The report records agent exit status, output hashes, verification results, and whether both stages passed. This is **not a sandbox**, and task allowed paths are **not enforced**. The agent executes on your host with your permissions. Task and check definitions are now validated and snapshotted **before** agent execution; changes to either input after the agent runs cause the run to fail without executing verification. Checks run from the pre-agent command snapshot. This does **not** make the underlying test code, dependencies, environment, or workspace immutable, and does not protect against concurrent filesystem races. Independently review the resulting code and tests before trusting the outcome. Do not pass secrets in command arguments, run on sensitive workspaces, or treat a passing report as permission to merge. CI uses mocked agent execution only. The command does not create branches, PRs, or merges.
