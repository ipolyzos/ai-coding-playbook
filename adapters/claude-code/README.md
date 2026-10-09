# Claude Code adapter

Claude Code commonly uses a project-level `CLAUDE.md`. Copy [CLAUDE.example.md](CLAUDE.example.md) to `CLAUDE.md` at the target repository root. Adapt the paths for your installation.

When starting a task, explicitly reference a prompt from the [catalog](../../prompts/README.md), supply repository context and acceptance criteria, and review the resulting diff.

This adapter does not configure hooks, permissions, or tool access. Set those separately according to your organization's policies.
