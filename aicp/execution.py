"""Explicitly approved, non-sandboxed task execution and verification."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

from .task_lifecycle import show_task
from .verification import verify


def run_task(project, name, tool, argv, checks_path, output, timeout=300):
    if tool not in ("codex", "claude", "gemini"):
        raise ValueError("Only explicitly supported local agent CLIs may run")
    if not argv or argv[0] != tool or not all(isinstance(a, str) and a for a in argv):
        raise ValueError("Agent argv must begin with selected tool")
    if type(timeout) is not int or not 1 <= timeout <= 1800:
        raise ValueError("Agent timeout must be between 1 and 1800 seconds")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Refusing to overwrite execution report")
    task = show_task(project, name)
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=project, capture_output=True, timeout=timeout, check=False)
        status, exit_code, stdout, stderr = "completed", proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        status, exit_code, stdout, stderr = "timeout", None, exc.stdout or b"", exc.stderr or b""
    except OSError as exc:
        status, exit_code, stdout, stderr = "launch_error", None, b"", str(exc).encode()
    agent = {
        "tool": tool,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "passed": status == "completed" and exit_code == 0,
    }
    # Never execute verification if agent execution itself failed.
    checks = verify(project, checks_path) if agent["passed"] else None
    report = {
        "schema_version": 1,
        "task": name,
        "objective": task["objective"],
        "agent": agent,
        "verification": checks,
        "passed": bool(agent["passed"] and checks and checks["passed"]),
        "security_boundary": "trusted-host-execution-no-sandbox",
        "scope_enforced": False,
    }
    with output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    return report
