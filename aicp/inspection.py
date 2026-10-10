"""Read-only inventory of existing AI assistant instruction entrypoints."""
from pathlib import Path

from .entrypoints import ENTRYPOINTS

ROOT_INSTRUCTIONS = "AGENTS.md"


def inspect_project(project):
    if not project.is_dir() or project.is_symlink():
        raise ValueError("Target must be an existing directory")
    paths = [ROOT_INSTRUCTIONS] + [value for value in ENTRYPOINTS.values() if value]
    files = []
    for relative in paths:
        target = project / relative
        parts = Path(relative).parts[:-1]
        parent = project
        unsafe = False
        for part in parts:
            parent = parent / part
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                unsafe = True
                break
        if unsafe or target.is_symlink():
            status = "unsafe"
        elif target.is_file():
            status = "present"
        elif target.exists():
            status = "conflict"
        else:
            status = "missing"
        files.append({"path": relative, "status": status})
    existing = [item["path"] for item in files if item["status"] == "present"]
    return {
        "schema_version": 1,
        "target": str(project),
        "files": files,
        "existing_instructions": existing,
        "requires_manual_review": bool(existing) or any(item["status"] in ("unsafe", "conflict") for item in files),
        "read_only": True,
    }
