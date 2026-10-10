# Agent task protocol (initial version)

A benchmark task defines the work request, a submitted workspace, and independent acceptance checks. The agent is **not** invoked by this harness; a human or external adapter supplies the workspace. Agent identity and execution provenance are not verified.

## Demonstration

The example task asks an agent to implement `solution.py` that reads `input.txt` and writes uppercase bytes to `result.txt`. The included solution is a known-good infrastructure fixture, **not** an agent-generated solution.

```sh
python3 scripts/verify_agent_submission.py evaluations/agent-tasks/uppercase-copy.json --submission evaluations/benchmarks/fixtures/copy-task --output /tmp/playbook-agent-evidence.json
```

This requires Docker and an available image. The checker runs the acceptance command in a restricted Docker container, then independently compares generated artifacts with pinned digests. A passing result verifies the submission against the stated checks only; it does not establish that an AI agent authored it, general correctness, or resistance to adversarial submissions.

## Threat model

A submission may contain arbitrary code. This container configuration is **not a hardened sandbox**. Run only reviewed submissions on a dedicated disposable host without credentials. Do not run untrusted third-party code on a developer workstation or a privileged Docker daemon. The current runner also copies submitted files into a temporary directory; keep submissions small and free of secrets.

Next steps: immutable task fixtures, hidden acceptance tests, verified adapter execution traces, and aggregate comparisons across tools.

For manually recording declared coding-agent metadata, transcript hashes, and workspace fingerprints, see [run provenance](PROVENANCE.md). This records claims; it does not authenticate agent identity.

For opt-in execution of an installed coding-agent CLI on a dedicated host, see [experimental CLI adapter](CLI_ADAPTER.md). It is not a security sandbox and does not run in CI.

To combine opt-in CLI execution with Docker acceptance verification and produce a structured report, see [experimental orchestration](ORCHESTRATION.md).
