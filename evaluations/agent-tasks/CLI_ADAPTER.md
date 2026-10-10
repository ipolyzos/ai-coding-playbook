# Opt-in coding-agent CLI execution (experimental)

`scripts/run_agent_cli.py` runs a selected CLI executable on a **trusted disposable host** and records the actual subprocess exit status, duration, stdout/stderr hashes, and before/after workspace fingerprints. It does not persist raw output.

Supported executable names: `codex`, `claude`, `gemini`. The tool must already be installed and available on `PATH`. No particular CLI arguments or vendor permission modes are assumed; review your installed version's documentation before use.

Example invocation (illustrative; requires a working Codex installation and appropriate local configuration):

```sh
python3 scripts/run_agent_cli.py --tool codex --task uppercase-copy --workspace /path/to/disposable-workspace --output /tmp/codex-run.json -- codex exec "Implement the task in TASK.md"
```

**Security warning:** An allowed executable name is not an allowlist of actions. Agents may run arbitrary commands, modify files outside the workspace, access the network, or interact with services. This runner does not sandbox the agent, enforce approvals, or independently verify authorship. It inherits a reduced environment (`PATH`, temporary `HOME`, `TMPDIR`) and deliberately does not forward API keys. Some CLIs may fail without authentication or configuration. Command arguments and workspace paths are written into evidence; do not include secrets. The timeout limits the direct CLI process but cannot guarantee termination of its descendants.

Never run untrusted tasks on a workstation with sensitive data or credentials. Use a dedicated, externally isolated host and manually review agent permission flags. Independently verify submissions using the [task protocol](README.md); a zero exit code alone is not task success. CI tests use mocks and do **not** invoke any agent CLI.
