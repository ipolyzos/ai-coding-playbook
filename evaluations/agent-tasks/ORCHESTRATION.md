# Experimental end-to-end agent benchmark

The orchestrator composes two existing steps: opt-in agent CLI execution and independent Docker-based acceptance verification. It writes separate `execution.json`, `acceptance.json` (only when attempted), and `report.json` records. A successful agent CLI exit code is **not** sufficient for benchmark success.

Example (requires Docker, an installed/authenticated agent CLI, a reviewed task manifest, and a disposable isolated machine):

```sh
python3 scripts/run_agent_benchmark.py evaluations/agent-tasks/uppercase-copy.json \
  --tool codex --workspace /path/to/disposable-workspace \
  --output-dir /tmp/playbook-benchmark-run -- \
  codex exec "Implement the task in TASK.md"
```

**Safety:** This is not a hardened sandbox. The agent CLI runs on the host and may access network or files outside its workspace. Docker restrictions apply only to the subsequent acceptance stage. Use an externally isolated disposable host without credentials or sensitive data, with reviewed vendor permission flags. The acceptance runner is also not a hardened sandbox. CI unit tests mock execution and do not launch agents or Docker. A run's tool name is not authenticated, and benchmark scores are meaningful only for identical task baselines and acceptance criteria.

This initial orchestration deliberately skips acceptance if agent execution fails, so reports clearly distinguish execution failures from acceptance failures. Exceptions in either stage propagate rather than being silently scored as passes.
