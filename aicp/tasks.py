"""Create structured, reviewable engineering task drafts."""
import json
from pathlib import Path
import re

DEFAULT_FORBIDDEN = ["deploy", "delete branches", "change repository permissions"]
DEFAULT_APPROVALS = ["merge pull request", "expand scope"]


def create_task(project, name, objective, allowed_paths, acceptance):
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Task name must be lowercase kebab-case")
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("Objective must not be empty")
    if not allowed_paths or not acceptance:
        raise ValueError("At least one allowed path and acceptance criterion are required")
    for path in allowed_paths:
        if not isinstance(path, str) or not path.strip() or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("Allowed paths must be nonempty relative paths without '..'")
    if any(not isinstance(item, str) or not item.strip() for item in acceptance):
        raise ValueError("Acceptance criteria must be nonempty")
    task = {
        "objective": objective.strip(),
        "scope": {
            "allowed_paths": allowed_paths,
            "forbidden_actions": DEFAULT_FORBIDDEN,
        },
        "acceptance_criteria": acceptance,
        "approval_required": DEFAULT_APPROVALS,
    }
    target = project / "tasks" / (name + ".json")
    if target.exists() or target.is_symlink():
        raise FileExistsError("Task already exists: " + str(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as handle:
        json.dump(task, handle, indent=2)
        handle.write("\n")
    return target
