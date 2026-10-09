# Coding assistant adapters

The playbook is tool-neutral. These adapters are **installation guides**, not separate sources of engineering policy. The canonical rules live in [AGENTS.md](../AGENTS.md), [instructions](../instructions/engineering.md), and the [prompt catalog](../prompts/README.md).

| Assistant | Setup |
| --- | --- |
| Claude Code | [Claude Code](claude-code/README.md) |
| Codex | [Codex](codex/README.md) |
| Cursor | [Cursor](cursor/README.md) |
| GitHub Copilot | [Copilot](copilot/README.md) |
| Gemini CLI | [Gemini CLI](gemini-cli/README.md) |

## Install into an existing repository

1. Read the relevant adapter guide.
2. Copy the example entrypoint into your target repository at the documented location.
3. Adjust the relative links to point to a local copy of the playbook, or paste the necessary standards into the entrypoint. Do not assume remote links are automatically loaded.
4. Start a fresh assistant session and verify it reads the entrypoint and follows the requested prompt.
5. Keep tool-specific instructions short; edit shared engineering policy in one place.

**Security:** Tool instructions are advisory. Enforce authorization, CI checks, and branch protection outside the model.
