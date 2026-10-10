# Adopt the playbook in an existing repository

If a repository already contains assistant instructions, do not replace them with `aicp init`. Instead, from the playbook checkout:

```sh
python3 -m aicp inspect --path /path/to/project
python3 -m aicp adopt --tool codex --path /path/to/project --dry-run
python3 -m aicp adopt --tool codex --path /path/to/project
python3 -m aicp validate --path /path/to/project
```

Adoption creates only `.aicp.json` and `.aicp/PLAYBOOK.md`. It never edits `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or Copilot instructions. Existing instruction files remain authoritative. Review the sidecar and, **only if appropriate**, manually add a reference to `.aicp/PLAYBOOK.md` in the existing tool instruction file. No tool is guaranteed to load the sidecar automatically.

The command refuses to overwrite existing files, rejects unsafe instruction paths and symlinked sidecar parent directories, and requires at least one existing assistant instruction file. It is not a policy-merging engine, nor does it launch an agent.
