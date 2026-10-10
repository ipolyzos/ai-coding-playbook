# Practical walkthrough

This guide shows how to use AI Coding Playbook in a **fictional** Python service. All paths, names, tasks, and commands are examples; no organization-specific or personal information is needed.

## 1. Keep the playbook separate from your application

From your development directory:

```sh
git clone https://github.com/ipolyzos/ai-coding-playbook.git
cd ai-coding-playbook
```

The CLI runs from this checkout. Your application lives in another existing directory, such as `/path/to/sample-service`. The basic CLI uses Python's standard library; it does not install or authenticate a coding assistant.

## 2. Choose initialization or adoption

For a repository **without** assistant instructions, preview before creating files:

```sh
python3 -m aicp init --tool codex --path /path/to/sample-service --dry-run
python3 -m aicp init --tool codex --path /path/to/sample-service
python3 -m aicp validate --path /path/to/sample-service
```

Initialization creates `.aicp.json` and `AGENTS.md` (plus an assistant-specific entrypoint for supported tools where applicable). It refuses to overwrite existing files. See [generated entrypoints](TOOL_ENTRYPOINTS.md).

For a repository **with** assistant instructions, use the non-destructive alternative:

```sh
python3 -m aicp inspect --path /path/to/sample-service
python3 -m aicp adopt --tool codex --path /path/to/sample-service --dry-run
python3 -m aicp adopt --tool codex --path /path/to/sample-service
python3 -m aicp validate --path /path/to/sample-service
```

Adoption creates `.aicp.json` and `.aicp/PLAYBOOK.md`, without editing existing assistant instructions. The sidecar is **not automatically loaded**: review it and manually link it from the existing instructions only if appropriate. See [adoption](ADOPTION.md).

## 3. Create a bounded task

For a fictional retry-handling defect:

```sh
python3 -m aicp task create \
  --path /path/to/sample-service \
  --name fix-retry-handling \
  --objective 'Prevent duplicate processing after a transient failure' \
  --allow src/ \
  --allow tests/ \
  --accept 'Regression test reproduces the failure before the fix' \
  --accept 'Relevant tests pass after the fix'
```

This writes `tasks/fix-retry-handling.json`. Review the generated allowed paths, forbidden actions, and approval boundaries before delegating. Task creation does **not** execute an agent.

## 4. Work interactively with a coding assistant

Open the application in your chosen coding assistant and supply the following request:

> Read the repository's assistant instructions and `tasks/fix-retry-handling.json`. Inspect the relevant code and propose a minimal plan before editing. Work only within the allowed paths. Add a regression test, run relevant checks, and report exact results. Do not expand scope, deploy, or merge without approval.

For other activities, choose the appropriate template from the [prompt catalog](../prompts/README.md): exploration, design, implementation, debugging, testing, or review. Verify that the assistant actually loaded the intended instructions; generating an entrypoint does not prove that it did.

## 5. Independently verify the result

Create `/path/to/sample-service/checks.json`:

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
  --path /path/to/sample-service \
  --checks /path/to/sample-service/checks.json \
  --output /tmp/sample-service-verification.json
```

AICP records command status, exit codes, duration, and output digests, rather than raw command output. **Review checks first:** they execute with your host permissions, not in a sandbox. The evidence file must not already exist. See [verification](VERIFICATION.md).

## 6. Review and integrate

The recommended lifecycle is: define task → review plan → implement on a feature branch → verify locally → open a PR → wait for CI → review changes → merge. The basic AICP commands do **not** create branches, open PRs, or merge; use your normal Git and hosting workflow for those steps.

## 7. Experimental autonomous execution

For advanced experiments, the repository includes an opt-in agent CLI adapter and a Docker-based acceptance stage. These are separate from `aicp task create` and `aicp verify`. The agent CLI can access host resources, and Docker acceptance is not a hardened sandbox. Use a disposable isolated machine with no credentials or sensitive data. See [experimental orchestration](../evaluations/agent-tasks/ORCHESTRATION.md).

## Next steps

Try one small, reversible task before expanding to larger changes. Compare the resulting diff, tests, and review effort with your usual workflow. See [workflow examples](WORKFLOWS.md) for more task patterns.
