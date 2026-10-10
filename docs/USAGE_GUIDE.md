# Practical usage guide

This guide shows how to use AI Coding Playbook (AICP) with an existing software repository. All names, paths, tasks, and examples below are fictional. No real users, employers, customers, internal systems, tokens, or private repositories are referenced.

## What AICP does

AICP provides reusable engineering prompts, assistant instruction entrypoints, bounded task definitions, and explicit verification evidence. It supports interactive development and experimental agent benchmarking. **It does not automatically implement tasks, install vendor CLIs, create PRs, or merge code.** Tool instructions are advisory; review and CI remain essential.

For a **tested, runnable version** of this walkthrough using a synthetic Python service, see [the practical example](../examples/practical/README.md). It includes a sample module, tests, a verification configuration, and disposable-directory setup commands.

## 1. Keep the playbook separate from your application

From a terminal with Python 3:

```sh
mkdir -p ~/dev
cd ~/dev
git clone https://github.com/ipolyzos/ai-coding-playbook.git
mkdir -p sample-service
cd ai-coding-playbook
```

Run `python3 -m aicp` from the playbook checkout in the following examples. Replace `../sample-service` with the path to an existing project directory.

## 2. Initialize a project without assistant instructions

Preview the proposed files before writing:

```sh
python3 -m aicp init --tool codex --path ../sample-service --dry-run
python3 -m aicp init --tool codex --path ../sample-service
python3 -m aicp validate --path ../sample-service
```

Codex uses `AGENTS.md`. Claude Code, Cursor, Copilot, and Gemini CLI use additional entrypoints, as documented in [tool entrypoints](TOOL_ENTRYPOINTS.md). Initialization refuses to overwrite existing target files. Validation checks configuration and instruction presence; it does not prove an assistant read them.

### Existing project with instructions: adopt instead

```sh
python3 -m aicp inspect --path ../sample-service
python3 -m aicp adopt --tool codex --path ../sample-service --dry-run
python3 -m aicp adopt --tool codex --path ../sample-service
python3 -m aicp validate --path ../sample-service
```

Adoption is appropriate only if the repository already has recognized assistant instructions. It creates `.aicp.json` and `.aicp/PLAYBOOK.md`, without changing existing instructions. Review the sidecar and explicitly reference it from the existing instructions **only if compatible with repository policy**. The sidecar is not loaded automatically. See [adoption](ADOPTION.md).

## 3. Interactive workflow: fix a retry defect

Create a scoped task:

```sh
python3 -m aicp task create \
  --path ../sample-service \
  --name fix-retry \
  --objective "Correct retry handling without changing successful requests" \
  --allow src/ \
  --allow tests/ \
  --accept "A regression test reproduces the original failure" \
  --accept "Relevant tests pass"
```

This writes `../sample-service/tasks/fix-retry.json`. Open your project in the assistant and provide a prompt such as:

> Read AGENTS.md (or the existing assistant instructions) and tasks/fix-retry.json. First inspect the relevant code and explain the failure and proposed minimal change. Wait for plan approval before editing. Change only allowed paths, add a regression test, run relevant checks, and report exact commands and results. Do not deploy, expand scope, or merge without approval.

AICP creates the task file; **you** provide it to the assistant. The assistant's actual behavior depends on its vendor, permissions, and configuration. Use [debug](../prompts/interactive/debug.md), [implement](../prompts/interactive/implement.md), and [review](../prompts/interactive/review.md) prompts as needed.

## 4. Independent verification workflow

In the sample project, create `checks.json` with **reviewed, trusted** commands:

```json
{
  "schema_version": 1,
  "checks": [
    ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"]
  ]
}
```

Then, from the playbook checkout:

```sh
python3 -m aicp verify \
  --path ../sample-service \
  --checks ../sample-service/checks.json \
  --output /tmp/sample-service-checks.json
```

Inspect the JSON report and any actual test failures. It records command status, exit codes, timing, and output digests, not raw logs. The verifier runs commands on the host with your user privileges: **it is not a sandbox**. Never run unreviewed commands or pass credentials in arguments. See [verification](VERIFICATION.md).

## 5. Example feature workflow: add a health endpoint

For a different task, create `add-health-endpoint` with objective `Add a read-only health endpoint`, allowed paths `src/` and `tests/`, and criteria such as `Healthy responses return HTTP 200` and `Endpoint tests pass`. Ask the assistant to inspect routing conventions, propose the smallest change, add tests, and report evidence. Review the diff and keep the change on a feature branch.

## 6. Example documentation-only workflow

For a documentation correction, use the [review prompt](../prompts/interactive/review.md) to identify inaccurate statements, then the [implementation prompt](../prompts/interactive/implement.md) to make a narrowly scoped change. Limit the task to `docs/`, check relative links, and confirm no runtime code was changed. Create a PR and use repository CI before merging.

## 7. Git and CI workflow

AICP does not create or merge PRs. A practical repository workflow is:

1. Start a short-lived feature branch from the latest `main`.
2. Create a bounded task and review the assistant's plan.
3. Implement incrementally and inspect each diff.
4. Run trusted local checks with `aicp verify`.
5. Push the branch and open a pull request using your existing Git tooling.
6. Wait for CI, address review comments, and merge only when required checks pass.

Use [autonomous task intake](../prompts/autonomous/task-intake.md) and [validation loop](../prompts/autonomous/validation-loop.md) for bounded delegation. These are templates, not an automatic authorization or enforcement system.

## 8. Experimental autonomous benchmarking

The optional [agent orchestration guide](../evaluations/agent-tasks/ORCHESTRATION.md) describes running an installed, authenticated agent CLI against a disposable workspace, followed by Docker-based acceptance verification. It is **not a hardened sandbox**: agent execution may access the host or network. Use only a separate, disposable environment without sensitive data or credentials. Normal interactive usage does not require Docker.

## Privacy and safe examples

Use synthetic repository names, paths, issue descriptions, test data, and logs in public documentation. Never include real names, email addresses, private company names, customer data, internal hostnames, API keys, tokens, credentials, or confidential source code. Review assistant transcripts and generated reports before sharing; command arguments, paths, and metadata may reveal sensitive information. Do not commit local `.env` files, secrets, or private verification outputs. Existing repository policies and organizational controls take precedence.

## Next reading

[CLI](CLI.md) · [Adoption](ADOPTION.md) · [Tool entrypoints](TOOL_ENTRYPOINTS.md) · [Verification](VERIFICATION.md) · [Prompt catalog](../prompts/README.md) · [Task contracts](../contracts/README.md)
