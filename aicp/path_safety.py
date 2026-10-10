"""Conservative checks for repository-relative filesystem operations."""
from pathlib import Path


def require_project(project):
    if not project.is_dir() or project.is_symlink():
        raise ValueError("Project must be an existing non-symlink directory")


def require_safe_path(project, relative):
    """Reject symlinked/non-directory parents and symlinked leaf paths.

    This is a preflight check, not a defense against concurrent filesystem
    changes by an adversarial process.
    """
    require_project(project)
    relative = Path(relative)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise ValueError("Expected a project-relative path without '..'")
    current = project
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise ValueError("Unsafe destination parent: " + str(current))
    target = project / relative
    if target.is_symlink():
        raise ValueError("Symlinked destination: " + str(target))
    return target
