# Codex adapter

Codex can use repository-level `AGENTS.md` instructions. Copy the canonical [AGENTS.md](../../AGENTS.md) into the target repository root, and bring in the relevant `instructions/`, `prompts/`, and `contracts/` folders.

Use the task prompt explicitly in your request; do not assume the assistant automatically selects a prompt file. Check the resolved instruction hierarchy in your Codex environment.

Avoid duplicating policy in a separate adapter-specific document.
