#!/usr/bin/env python3
"""Run trusted benchmark definitions inside a restricted Docker container.

This is defense in depth, not a guarantee against container escape.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_benchmark import execute


def docker_argv(image, workspace, command):
    if not isinstance(image, str) or not image or any(c.isspace() for c in image):
        raise ValueError("A nonempty Docker image reference is required")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ValueError("Command must be a nonempty argv list")
    return [
        "docker", "run", "--rm", "--network", "none",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--read-only", "--pids-limit", "64", "--memory", "256m",
        "--cpus", "1", "--user", "65534:65534",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=32m",
        "--mount", f"type=bind,src={workspace.resolve()},dst=/workspace,rw",
        "--workdir", "/workspace", image, *command,
    ]


def run(definition, fixture, output):
    if not fixture.is_dir() or fixture.is_symlink():
        raise ValueError("Fixture must be a real directory")
    if any(p.is_symlink() for p in fixture.rglob("*")):
        raise ValueError("Fixture must not contain symlinks")
    expected = definition.get("expected_files")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("expected_files must map paths to SHA-256 digests")
    for path, digest in expected.items():
        p = Path(path)
        if not path or p.is_absolute() or ".." in p.parts or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid artifact path or SHA-256 digest")
    with tempfile.TemporaryDirectory(prefix="playbook-container-") as temp:
        workspace = Path(temp) / "workspace"
        shutil.copytree(fixture, workspace)
        if any(p.is_symlink() for p in workspace.rglob("*")):
            raise ValueError("Workspace contains symlinks")
        # Unprivileged container user needs write access to the disposable workspace.
        workspace.chmod(0o777)
        for p in workspace.rglob("*"):
            if p.is_dir():
                p.chmod(0o777)
            else:
                p.chmod(0o666)
        argv = docker_argv(definition["image"], workspace, definition["command"])
        evidence = execute({"id": definition["id"], "command": argv, "timeout_seconds": definition["timeout_seconds"]}, Path(temp), output)
        assertions = {}
        for relative, digest in expected.items():
            artifact = workspace / relative
            assertions[relative] = artifact.is_file() and not artifact.is_symlink() and artifact.resolve().is_relative_to(workspace.resolve()) and hashlib.sha256(artifact.read_bytes()).hexdigest() == digest
        result = {**evidence, "assertions": assertions, "passed": evidence["passed"] and all(assertions.values()), "execution_mode": "docker-restricted"}
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("definition", type=Path)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(json.loads(args.definition.read_text()), args.fixture, args.output)
    print(json.dumps({"benchmark": result["benchmark"], "passed": result["passed"], "evidence": str(args.output)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
