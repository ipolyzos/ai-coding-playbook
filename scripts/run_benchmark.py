#!/usr/bin/env python3
"""Run an explicitly configured local benchmark command and record verifiable evidence.

This runner does not execute agents, accept shell strings, or claim sandbox isolation.
Use only trusted benchmark definitions in a controlled environment.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def execute(definition, cwd, output):
    command = definition["command"]
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ValueError("command must be a nonempty argument array")
    timeout = definition["timeout_seconds"]
    if type(timeout) is not int or not 1 <= timeout <= 300:
        raise ValueError("timeout_seconds must be an integer between 1 and 300")
    if not cwd.is_dir():
        raise ValueError("working directory does not exist")
    started = time.monotonic()
    status = "completed"
    exit_code = None
    try:
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
        exit_code = proc.returncode
        stdout, stderr = proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        status = "timeout"
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
    except OSError as exc:
        status = "launch_error"
        stdout, stderr = "", str(exc)
    elapsed = round(time.monotonic() - started, 3)
    # Do not persist raw output: it may contain secrets or user data.
    evidence = {
        "schema_version": 1,
        "benchmark": definition["id"],
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "command": command,
        "cwd": str(cwd.resolve()),
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": elapsed,
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
        "stdout_bytes": len(stdout.encode()),
        "stderr_bytes": len(stderr.encode()),
        "passed": status == "completed" and exit_code == 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("definition", type=Path)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    definition = json.loads(args.definition.read_text(encoding="utf-8"))
    if not isinstance(definition.get("id"), str) or not definition["id"]:
        parser.error("benchmark id is required")
    result = execute(definition, args.cwd, args.output)
    print(json.dumps({"benchmark": result["benchmark"], "passed": result["passed"], "status": result["status"], "evidence": str(args.output)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
