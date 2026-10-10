#!/usr/bin/env python3
"""Opt-in local CLI adapter for trusted coding assistants.

This does NOT sandbox a coding agent. Use only on a disposable machine and with
explicit authorization. No agent is launched by CI.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.record_agent_run import fingerprint

ALLOWED_TOOLS = frozenset({"codex", "claude", "gemini"})


def validate_tool(tool, argv, timeout):
    if tool not in ALLOWED_TOOLS:
        raise ValueError("Unsupported tool; allowed: " + ", ".join(sorted(ALLOWED_TOOLS)))
    if not isinstance(argv, list) or not argv or argv[0] != tool or not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("argv must begin with the selected tool executable")
    if type(timeout) is not int or not 1 <= timeout <= 1800:
        raise ValueError("timeout must be between 1 and 1800 seconds")


def run_agent(tool, argv, task, workspace, output, timeout=300):
    validate_tool(tool, argv, timeout)
    if not workspace.is_dir() or workspace.is_symlink():
        raise ValueError("Workspace must be an existing directory")
    if not isinstance(task, str) or not task.strip():
        raise ValueError("Task id must be nonempty")
    before, _ = fingerprint(workspace)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="playbook-agent-") as temp:
        home = Path(temp)
        # Only explicitly selected variables are inherited. Tool authentication
        # is not provided; users must arrange it separately in a disposable host.
        env = {"PATH": os.environ.get("PATH", ""), "HOME": str(home), "TMPDIR": str(home)}
        if os.name == "nt":
            raise ValueError("This adapter currently supports POSIX hosts only")
        try:
            proc = subprocess.run(argv, cwd=workspace, env=env, capture_output=True, timeout=timeout, check=False)
            status, exit_code = "completed", proc.returncode
            stdout, stderr = proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            status, exit_code = "timeout", None
            stdout, stderr = exc.stdout or b"", exc.stderr or b""
        except OSError as exc:
            status, exit_code = "launch_error", None
            stdout, stderr = b"", str(exc).encode()
        elapsed = round(time.monotonic() - started, 3)
        after, count = fingerprint(workspace)
        result = {
            "schema_version": 1,
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "task": task,
            "tool": tool,
            "argv": argv,
            "identity_verification": "executable-name-only",
            "execution_verified": status == "completed",
            "status": status,
            "exit_code": exit_code,
            "duration_seconds": elapsed,
            "workspace_before_sha256": before,
            "workspace_after_sha256": after,
            "workspace_file_count": count,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stdout_bytes": len(stdout),
            "stderr_bytes": len(stderr),
            "passed": status == "completed" and exit_code == 0,
        }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", choices=sorted(ALLOWED_TOOLS), required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("argv", nargs=argparse.REMAINDER, help="Command after --, starting with the tool name")
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv and args.argv[0] == "--" else args.argv
    result = run_agent(args.tool, argv, args.task, args.workspace, args.output, args.timeout)
    print(json.dumps({"tool": result["tool"], "status": result["status"], "evidence": str(args.output)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
