"""Opt-in, non-destructive adoption for repositories with existing instructions."""
import json
from pathlib import Path

from .entrypoints import ENTRYPOINTS
from .inspection import inspect_project

SIDECAR = ".aicp/PLAYBOOK.md"
CONFIG = ".aicp.json"


def plan_adoption(project, tool):
    if tool not in ENTRYPOINTS:
        raise ValueError("Unsupported tool")
    inventory = inspect_project(project)
    existing = inventory["existing_instructions"]
    if not existing:
        raise ValueError("No existing assistant instructions found; use 'aicp init' instead")
    files = []
    for relative in (CONFIG, SIDECAR):
        target = project / relative
        parent = target.parent
        unsafe = False
        while parent != project:
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                unsafe = True
                break
            parent = parent.parent
        files.append({"path": relative, "action": "blocked" if unsafe or target.exists() or target.is_symlink() else "create"})
    return {
        "schema_version": 1,
        "tool": tool,
        "existing_instructions": existing,
        "ready": all(item["action"] == "create" for item in files)
        and not any(item["status"] in ("unsafe", "conflict") for item in inventory["files"]),
        "files": files,
        "dry_run": True,
    }


def adopt(project, tool):
    plan = plan_adoption(project, tool)
    if not plan["ready"]:
        raise FileExistsError("Adoption blocked; inspect existing paths and retry")
    sidecar = project / SIDECAR
    config = project / CONFIG
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "# AI Coding Playbook — optional engineering guidance\n\n"
        "Work in small scoped changes, define acceptance criteria, test relevant behavior, "
        "and report verification evidence accurately. Obtain explicit approval for destructive "
        "operations, deployments, and permission changes. Existing repository instructions "
        "remain authoritative.\n\n"
        "This file is NOT automatically loaded by coding assistants. To opt in, manually "
        "reference .aicp/PLAYBOOK.md from your existing assistant instruction file after "
        "reviewing it for compatibility with project policy.\n"
    )
    with sidecar.open("x", encoding="utf-8") as handle:
        handle.write(text)
    try:
        with config.open("x", encoding="utf-8") as handle:
            json.dump({"schema_version": 1, "tool": tool, "instructions": SIDECAR, "mode": "adopt"}, handle, indent=2)
            handle.write("\n")
    except BaseException:
        sidecar.unlink()
        raise
    return config
