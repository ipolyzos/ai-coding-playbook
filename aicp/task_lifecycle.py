"""Read and validate local task drafts without executing them."""
import json
from pathlib import Path
import re

from .path_safety import require_safe_path


def _task_path(project, name):
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Task name must be lowercase kebab-case")
    return require_safe_path(project, Path("tasks") / (name + ".json"))


def validate_task_data(task):
    if not isinstance(task, dict) or set(task) != {"objective", "scope", "acceptance_criteria", "approval_required"}:
        raise ValueError("Invalid task contract fields")
    if not isinstance(task["objective"], str) or not task["objective"].strip():
        raise ValueError("Task objective must be nonempty")
    scope = task["scope"]
    if not isinstance(scope, dict) or set(scope) != {"allowed_paths", "forbidden_actions"}:
        raise ValueError("Invalid task scope")
    paths = scope["allowed_paths"]
    if not isinstance(paths, list) or not paths:
        raise ValueError("Task requires allowed paths")
    for path in paths:
        if not isinstance(path, str) or not path.strip() or Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError("Invalid allowed path")
    for key, values, nonempty in (
        ("forbidden_actions", scope["forbidden_actions"], False),
        ("acceptance_criteria", task["acceptance_criteria"], True),
        ("approval_required", task["approval_required"], False),
    ):
        if not isinstance(values, list) or (nonempty and not values) or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError("Invalid " + key)
    return task


def show_task(project, name):
    path = _task_path(project, name)
    if not path.is_file():
        raise ValueError("Task not found: " + name)
    return validate_task_data(json.loads(path.read_text(encoding="utf-8")))


def list_tasks(project):
    directory = require_safe_path(project, "tasks")
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise ValueError("Task directory is not a directory")
    names = []
    for path in sorted(directory.iterdir()):
        if path.suffix != ".json":
            continue
        name = path.stem
        show_task(project, name)
        names.append(name)
    return names
