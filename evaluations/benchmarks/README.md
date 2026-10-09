# Executable evidence foundation

The benchmark runner executes a **trusted, explicit argv command** and saves a JSON evidence record with exit code, status, elapsed time, and SHA-256 digests of stdout/stderr. It does not save raw output. It deliberately does **not** run AI agents, validate the correctness of agent-produced code, redact command arguments, or provide a security sandbox.

## Local smoke test

```sh
python3 scripts/run_benchmark.py evaluations/benchmarks/stdlib-smoke.json --cwd . --output /tmp/playbook-smoke-evidence.json
```

The smoke test proves only that command execution and evidence recording work. Never report it as a measured coding-agent benchmark.

## Security and interpretation

- Run only reviewed benchmark definitions. The argv array can execute arbitrary programs; avoiding a shell is **not** a sandbox.
- Use a disposable workspace with restricted credentials, network access, and filesystem permissions for untrusted code.
- Command arguments and working-directory paths are stored verbatim in evidence; never put secrets in them.
- SHA-256 digests prove consistency of observed output bytes, not correctness or absence of secret leakage.
- Evidence files may include sensitive local paths. Review before sharing.
- A passing exit code is not proof of acceptance criteria. Combine with independent test assertions, diff review, and explicit authorization checks.

## Next iteration

Add isolated repository fixtures, agent adapters, assertions against produced artifacts, and baseline comparisons. Keep those separate from this infrastructure-only smoke test.
