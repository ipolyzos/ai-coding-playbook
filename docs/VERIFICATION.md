# Local verification with AICP

AICP can execute **explicit, reviewed commands** in a project and emit structured evidence. This is not a sandbox. Only use with trusted repositories and trusted checks.

Create `checks.json` in your initialized project:

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
python3 -m aicp verify --path /path/to/project --checks /path/to/project/checks.json --output /tmp/aicp-checks.json
```

Commands execute sequentially as argv arrays without shell interpolation. Every command is attempted, including after a failure; the overall result passes only if all checks exit zero. Timeouts and launch errors fail closed. The report includes exit codes, elapsed time, and output digests, **not raw output**. Review commands before running them: they have the same host privileges as the invoking user and may change files or access secrets. Subprocess timeout is not a process-tree containment mechanism. Avoid passing secrets as command arguments because argv is recorded in the report. The CLI does not automatically discover or invent test commands.

## Diagnostic summaries

Verification evidence includes a `summary` object with total, passed, failed, timed-out, and launch-error counts. The CLI prints the counts and failing check indices/statuses without printing captured stdout or stderr. The JSON still records command arguments and hashes, which may reveal sensitive values: only use reviewed commands without secrets in arguments, and keep reports private when appropriate. Timeouts bound the direct subprocess call but are **not a guarantee that all descendant processes are terminated**. This is trusted host execution, not isolation.
