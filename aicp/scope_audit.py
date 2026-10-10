"""Best-effort Git working-tree change auditing (not filesystem enforcement)."""
import subprocess
from pathlib import PurePosixPath


def git_snapshot(project):
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=project, capture_output=True, check=False, timeout=30,
    )
    if proc.returncode:
        raise ValueError("Git status failed; scope audit requires a Git worktree")
    entries = proc.stdout.split(b"\0")
    paths = set()
    i = 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if not entry:
            continue
        if len(entry) < 4:
            raise ValueError("Unexpected Git status output")
        path = entry[3:].decode("utf-8", errors="surrogateescape")
        paths.add(path)
        if entry[:1] in (b"R", b"C") or entry[1:2] in (b"R", b"C"):
            if i >= len(entries) or not entries[i]:
                raise ValueError("Incomplete Git rename entry")
            paths.add(entries[i].decode("utf-8", errors="surrogateescape"))
            i += 1
    return paths


def audit_scope(before, after, allowed_paths):
    added = sorted(after - before)
    allowed = []
    outside = []
    for path in added:
        parts = PurePosixPath(path).parts
        match = any(
            path == prefix.rstrip("/") or path.startswith(prefix.rstrip("/") + "/")
            for prefix in allowed_paths
        )
        (allowed if match else outside).append(path)
    return {
        "newly_reported_paths": added,
        "within_allowed_paths": allowed,
        "outside_allowed_paths": outside,
        "preexisting_changed_paths": sorted(before),
        "passed": not outside,
        "limitations": "git-status-delta-only; does not detect modifications to already dirty files, committed changes, ignored files, or reverted writes",
    }
