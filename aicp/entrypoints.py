"""Conservative, non-overwriting tool instruction entrypoints."""
from pathlib import Path

ENTRYPOINTS = {
    "codex": None,  # AGENTS.md is already created by init.
    "claude": "CLAUDE.md",
    "cursor": ".cursor/rules/ai-coding-playbook.mdc",
    "copilot": ".github/copilot-instructions.md",
    "gemini": "GEMINI.md",
}


def render(tool):
    if tool == "cursor":
        return (
            "---\ndescription: AI Coding Playbook engineering expectations\nalwaysApply: true\n---\n\n"
            "Follow the repository's AGENTS.md engineering instructions. "
            "Use scoped changes, tests, and evidence. Ask before destructive actions.\n"
        )
    return (
        "# AI Coding Playbook\n\n"
        "Follow the engineering instructions in AGENTS.md at the repository root. "
        "Use explicit scope, small reviewed changes, relevant tests, and truthful verification. "
        "Ask for authorization before destructive actions or deployments.\n"
    )


def install_entrypoint(project, tool):
    if tool not in ENTRYPOINTS:
        raise ValueError("Unsupported tool")
    relative = ENTRYPOINTS[tool]
    if relative is None:
        return project / "AGENTS.md", False
    path = project / relative
    if path.exists() or path.is_symlink():
        raise FileExistsError("Refusing to overwrite " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(render(tool))
    return path, True
