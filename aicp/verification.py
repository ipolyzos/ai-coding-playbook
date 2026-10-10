"""Explicit, bounded local verification of a repository's configured checks."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

MAX_TIMEOUT = 600
MAX_CHECKS = 20


def validate_checks(checks):
    if not isinstance(checks, list) or not checks or len(checks) > MAX_CHECKS:
        raise ValueError("Checks must be a nonempty list of at most 20 commands")
    for command in checks:
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise ValueError("Each check must be a nonempty argv list of strings")
    return checks


def run_checks(project, checks, timeout=120):
    validate_checks(checks)
    if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT:
        raise ValueError("Timeout must be between 1 and 600 seconds")
    if not project.is_dir() or project.is_symlink():
        raise ValueError("Project must be an existing directory")
    results = []
    for command in checks:
        started = time.monotonic()
        try:
            proc = subprocess.run(command, cwd=project, capture_output=True, timeout=timeout, check=False)
            status, exit_code, stdout, stderr = "completed", proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            status, exit_code, stdout, stderr = "timeout", None, exc.stdout or b"", exc.stderr or b""
        except OSError as exc:
            status, exit_code, stdout, stderr = "launch_error", None, b"", str(exc).encode()
        results.append({
            "argv": command,
            "status": status,
            "exit_code": exit_code,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "passed": status == "completed" and exit_code == 0,
        })
    return {"schema_version": 1, "passed": all(item["passed"] for item in results), "checks": results}


def verify(project, config_path, timeout=120):
    if not config_path.is_file() or config_path.is_symlink():
        raise ValueError("Checks configuration file must exist and must not be a symlink")
    resolved = config_path.resolve()
    root = project.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Checks configuration must be inside project")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or set(config) != {"schema_version", "checks"} or config["schema_version"] != 1:
        raise ValueError("Invalid checks configuration")
    return run_checks(project, config["checks"], timeout)
