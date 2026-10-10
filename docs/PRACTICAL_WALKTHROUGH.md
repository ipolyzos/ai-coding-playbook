# Practical walkthrough: from repository to reviewed PR

This guide shows how to use AI Coding Playbook with an existing Python project and Codex. The same engineering workflow applies to other supported assistants. The playbook provides instructions, task drafts, and verification; the basic CLI **does not automatically execute an agent, create a pull request, or merge changes**.

Prefer a fully runnable exercise? Start with the [synthetic Python example](../examples/practical/README.md), which includes tested code and a checks file.

## 1. Clone the playbook

```sh
git clone https://github.com/ipolyzos/ai-coding-playbook.git
cd ai-coding-playbook
```

Run the commands below **from the playbook checkout**, replacing `/path/to/project` with an existing project directory. The playbook and your application are separate repositories. Basic CLI commands use the Python standard library.

## 2. Initialize or adopt

For a project **without existing assistant instructions**, preview the files before writing:

```sh
python3 -m aicp init --tool codex --path /path/to/project --dry-run
python3 -m aicp init --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
```

Initialization creates `.aicp.json` and `AGENTS.md`. For other tools it also generates a short assistant-specific entrypoint where applicable: Claude Code `CLAUDE.md`, Cursor `.cursor/rules/ai-coding-playbook.mdc`, GitHub Copilot `.github/copilot-instructions.md`, and Gemini CLI `GEMINI.md`. It never overwrites existing target files.

For a project **with existing assistant instructions**, use the non-destructive alternative:

```sh
python3 -m aicp inspect --path /path/to/project
python3 -m aicp adopt --tool codex --path /path/to/project --dry-run
python3 -m aicp adopt --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
```

Adoption preserves existing instruction files and creates `.aicp.json` plus `.aicp/PLAYBOOK.md`. **The sidecar is not automatically loaded by your assistant**: review it and explicitly reference it from existing instructions if compatible with your project policy. See [adoption](ADOPTION.md) and [tool entrypoints](TOOL_ENTRYPOINTS.md).

## 3. Define a bounded engineering task

Suppose a Kafka consumer has a retry-handling bug. Create a structured task draft:

```sh
python3 -m aicp task create \
  --path /path/to/project \
  --name fix-consumer-retry \
  --objective "Fix Kafka consumer retry handling" \
  --allow src/ \
  --allow tests/ \
  --accept "Retries preserve message ordering" \
  --accept "Existing tests pass" \
  --accept "A regression test covers the defect"
```

This creates `tasks/fix-consumer-retry.json` with the objective, allowed paths, acceptance criteria, forbidden actions, and actions requiring approval. Review the generated draft and adapt its criteria to actual project behavior. The command **does not launch an agent**.

## 4. Work interactively with the assistant

Open the target repository in your coding assistant and provide a prompt such as:

> Read `AGENTS.md` (or the applicable assistant entrypoint) and `tasks/fix-consumer-retry.json`. Inspect the relevant code, explain the root cause, and propose a minimal implementation plan before editing. Work only within the allowed paths. Add a regression test, run the relevant checks, and report the exact results. Do not merge or expand scope without approval.

For repositories using `adopt`, first confirm the assistant is actually reading the manually linked sidecar. The [prompt catalog](../prompts/README.md) also contains focused exploration, design, debugging, implementation, testing, and review prompts.

## 5. Verify independently

Create `checks.json` in your target project (adapt the command to its actual test runner):

```json
{
  "schema_version": 1,
  "checks": [
    ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"]
  ]
}
```

Run from the playbook checkout:

```sh
python3 -m aicp verify \
  --path /path/to/project \
  --checks /path/to/project/checks.json \
  --output /tmp/aicp-verification.json
```

The report records command exit codes, durations, and output digests; it does not contain raw output. **This is not a sandbox**: reviewed commands run with the invoking user's permissions, and the output path must not already exist. See [verification details](VERIFICATION.md).

## 6. Review and merge through your normal Git workflow

A suggested lifecycle is:

1. Define the task and review the plan.
2. Implement on a focused feature branch.
3. Run project tests and AICP verification.
4. Open a pull request.
5. Require CI to pass and review the diff.
6. Merge only after the required checks and reviews succeed.

AICP's basic commands do not create feature branches, open PRs, or merge automatically. Use your existing GitHub tooling for those steps.

## 7. Optional experimental agent benchmarking

The repository also includes experimental scripts to invoke selected agent CLIs and independently assess work through Docker-based acceptance checks. This is **not a hardened unattended execution environment**: agent CLI execution runs on the host, and Docker restrictions apply only to the later acceptance stage. Use disposable isolated machines without credentials or sensitive data. See [agent orchestration](../evaluations/agent-tasks/ORCHESTRATION.md).

## Suggested first exercise

Choose one small, reproducible bug in a repository you know well. Adopt or initialize the playbook, write a narrowly scoped task, use an assistant interactively, run independent checks, and review the PR. This tests the full human-supervised workflow before experimenting with autonomous execution.
