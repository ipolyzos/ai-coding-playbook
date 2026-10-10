# Inspect an existing repository

Before adding AI Coding Playbook instructions to an existing project, run:

```sh
python3 -m aicp inspect --path /path/to/project
```

The command prints a read-only JSON inventory of root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, and Copilot instructions. Each entry is marked `present`, `missing`, `conflict`, or `unsafe` (including symlinked instruction paths or parent directories).

`requires_manual_review` is true if existing instructions or unsafe/conflicting paths are detected. Review project-specific rules and resolve conflicts manually; the inspector does not copy, rewrite, merge, or interpret the contents of existing instructions. It does not claim the playbook is installed or that any coding assistant has loaded instructions. For new initialization, use `aicp init --dry-run` first.
