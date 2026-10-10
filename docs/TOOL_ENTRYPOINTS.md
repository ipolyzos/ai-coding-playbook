# Tool-specific initialization

`python3 -m aicp init --tool TOOL --path PROJECT` creates the shared `AGENTS.md` and, where applicable, a short assistant-specific entrypoint.

| Tool | Generated entrypoint |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/ai-coding-playbook.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` |

All entrypoints refer to the root `AGENTS.md`, keeping engineering expectations in one place. Existing target files are not overwritten. This is an onboarding convenience, not proof that a vendor assistant loaded the file. Verify behavior in a fresh session. No agent is executed and no vendor CLI is installed.
