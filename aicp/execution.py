"""Explicitly approved, non-sandboxed task execution and verification."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

from .task_lifecycle import show_task
from .verification import run_checks, validate_checks


def _load_trusted_inputs(project, name, checks_path):
    """Snapshot the task and verification configuration before agent execution."""
    project_root = project.resolve()
    task_path = project / "tasks" / (name + ".json")
    if checks_path.is_symlink() or not checks_path.is_file():
        raise ValueError("Checks configuration must be a regular, non-symlink file")
    if not checks_path.resolve().is_relative_to(project_root):
        raise ValueError("Checks configuration must be inside project")
    task = show_task(project, name)
    task_bytes = task_path.read_bytes()
    checks_bytes = checks_path.read_bytes()
    config = json.loads(checks_bytes)
    if not isinstance(config, dict) or set(config) != {"schema_version", "checks"} or config["schema_version"] != 1:
        raise ValueError("Invalid checks configuration")
    checks = validate_checks(config["checks"])
    return task, task_path, task_bytes, checks_bytes, checks


def run_task(project, name, tool, argv, checks_path, output, timeout=300):
    if tool not in ("codex", "claude", "gemini"):
        raise ValueError("Only explicitly supported local agent CLIs may run")
    if not argv or argv[0] != tool or not all(isinstance(a, str) and a for a in argv):
        raise ValueError("Agent argv must begin with selected tool")
    if type(timeout) is not int or not 1 <= timeout <= 1800:
        raise ValueError("Agent timeout must be between 1 and 1800 seconds")
    if output.exists() or output.is_symlink():
        raise FileExistsError("Refusing to overwrite execution report")
    task, task_path, task_bytes, checks_bytes, trusted_checks = _load_trusted_inputs(project, name, checks_path)
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
    # Detect changes to the contract/configuration, and never execute a
    # replacement check list supplied by the agent.
    inputs_unchanged = (
        task_path.is_file() and not task_path.is_symlink()
        and checks_path.is_file() and not checks_path.is_symlink()
        and task_path.read_bytes() == task_bytes
        and checks_path.read_bytes() == checks_bytes
    )
    checks = run_checks(project, trusted_checks) if agent["passed"] and inputs_unchanged else None
    report = {
        "schema_version": 1,
        "task": name,
        "objective": task["objective"],
        "agent": agent,
        "verification": checks,
        "trusted_inputs": {
            "task_sha256": hashlib.sha256(task_bytes).hexdigest(),
            "checks_sha256": hashlib.sha256(checks_bytes).hexdigest(),
            "unchanged_after_agent": inputs_unchanged,
            "verification_source": "pre-agent-snapshot",
        },
        "passed": bool(agent["passed"] and inputs_unchanged and checks and checks["passed"]),
        "security_boundary": "trusted-host-execution-no-sandbox",
        "scope_enforced": False,
    }
    with output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    return report
