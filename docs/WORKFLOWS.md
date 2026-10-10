# Example engineering workflows

These scenarios are **fictional** and use generic paths. They do not describe any real user's employer, private repository, infrastructure, credentials, or projects. Commands assume you are in the AI Coding Playbook checkout and have already initialized or adopted a separate application repository. Replace the placeholder paths and test commands with reviewed equivalents for your own environment.

## Workflow A: Fix a retry defect

**Goal:** Fix duplicate processing after transient failures in a sample event consumer.

```sh
python3 -m aicp task create \
  --path /path/to/sample-service \
  --name prevent-duplicate-retries \
  --objective 'Prevent duplicate processing after transient errors' \
  --allow src/ --allow tests/ \
  --accept 'A regression test demonstrates the failure' \
  --accept 'Relevant unit tests pass'
```

Use [debug](../prompts/interactive/debug.md) to investigate and [test](../prompts/interactive/test.md) to design regression coverage. Ask the assistant to propose a plan, implement only approved changes, and report actual test results. Then run your independently reviewed checks using `aicp verify`, review the diff, and open a PR through your usual tooling.

## Workflow B: Implement a small API feature

**Goal:** Add an optional `limit` parameter to a fictional list endpoint without changing default behavior.

```sh
python3 -m aicp task create \
  --path /path/to/sample-service \
  --name add-list-limit \
  --objective 'Support an optional limit parameter on the list endpoint' \
  --allow src/ --allow tests/ --allow docs/ \
  --accept 'Omitting limit preserves existing behavior' \
  --accept 'Invalid limits return a documented error' \
  --accept 'Unit tests cover boundary cases'
```

Start with [design](../prompts/interactive/design.md), then [implementation](../prompts/interactive/implement.md) and [review](../prompts/interactive/review.md). Keep compatibility, validation, and tests within scope. Do not treat an assistant's claim that tests passed as independent evidence.

## Workflow C: Investigate flaky tests

**Goal:** Diagnose a nondeterministic unit test without broad production changes.

```sh
python3 -m aicp task create \
  --path /path/to/sample-service \
  --name stabilize-timeout-test \
  --objective 'Identify and remove nondeterminism from the timeout test' \
  --allow tests/ \
  --accept 'Root cause is documented with evidence' \
  --accept 'Repeated targeted test runs pass' \
  --accept 'No production source files are modified'
```

Use [explore](../prompts/interactive/explore.md) and [debug](../prompts/interactive/debug.md). Run a trusted repeat-test command manually or through `aicp verify`. If the fix requires production changes, stop and seek approval to expand the task scope.

## Workflow D: Onboard an established repository

**Goal:** Add playbook guidance without replacing existing assistant policies.

```sh
python3 -m aicp inspect --path /path/to/sample-service
python3 -m aicp adopt --tool claude --path /path/to/sample-service --dry-run
python3 -m aicp adopt --tool claude --path /path/to/sample-service
python3 -m aicp validate --path /path/to/sample-service
```

Review `.aicp/PLAYBOOK.md` against existing instructions. Only manually link the sidecar if compatible. The command does not merge policies or guarantee that Claude Code loads the sidecar.

## Workflow E: Independent verification and PR gate

Create a project-local `checks.json` with trusted commands:

```json
{
  "schema_version": 1,
  "checks": [
    ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"]
  ]
}
```

```sh
python3 -m aicp verify \
  --path /path/to/sample-service \
  --checks /path/to/sample-service/checks.json \
  --output /tmp/sample-verification.json
```

Review the resulting report and the code diff. Open a feature PR using your Git hosting tools; wait for successful CI and required review before merging. AICP does not automate those GitHub operations.

## Safety and privacy checklist

- Use synthetic names and fixtures in examples, bug reports, and shared transcripts.
- Never commit API keys, tokens, customer records, proprietary source, or raw agent transcripts to example repositories.
- Review command arguments, environment, and permissions before invoking any local verification or agent CLI.
- Keep agent experiments in disposable isolated environments; the experimental runner is not a hardened sandbox.
- Keep repository-specific rules authoritative, and require approval for scope expansion or destructive actions.

For the complete setup sequence, see [Practical walkthrough](PRACTICAL_WALKTHROUGH.md).
