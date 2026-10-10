"""Read-only preview of playbook initialization changes."""
from pathlib import Path

from .entrypoints import ENTRYPOINTS


def plan_init(project, tool):
    if tool not in ENTRYPOINTS:
        raise ValueError("Unsupported tool")
    if not project.is_dir() or project.is_symlink():
        raise ValueError("Target must be an existing directory")
    targets = [".aicp.json", "AGENTS.md"]
    if ENTRYPOINTS[tool]:
        targets.append(ENTRYPOINTS[tool])
    entries = []
    for relative in targets:
        path = project / relative
        parent = path.parent
        unsafe_parent = False
        while parent != project:
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                unsafe_parent = True
                break
            parent = parent.parent
        status = "blocked" if unsafe_parent or path.exists() or path.is_symlink() else "create"
        entries.append({"path": relative, "action": status})
    return {
        "schema_version": 1,
        "tool": tool,
        "target": str(project),
        "ready": all(entry["action"] == "create" for entry in entries),
        "files": entries,
        "dry_run": True,
    }
