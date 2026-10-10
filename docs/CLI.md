# AICP CLI (foundation)

Run directly from a checkout of the playbook, using the Python standard library:

```sh
python3 -m aicp init --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
python3 -m aicp --version
```

Supported tool labels: `codex`, `claude`, `cursor`, `copilot`, `gemini`. Initialization creates a minimal `AGENTS.md` and `.aicp.json` in an **existing** project directory. It never overwrites either file. Validation checks configuration shape and the presence of generated instructions; it does **not** enforce tool-specific policies, execute tests, or prove adherence to engineering standards.

This is a minimal, tool-neutral onboarding step. It does not install vendor CLIs, create tasks, or run agents. Future increments can provide vendor-specific setup, `task create`, and `verify` commands.
