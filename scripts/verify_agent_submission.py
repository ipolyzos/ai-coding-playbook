#!/usr/bin/env python3
"""Verify a submitted agent workspace against trusted, pinned acceptance checks.

The verifier does not launch an agent or execute untrusted submissions directly.
Only use this with trusted fixture scripts and restricted Docker execution.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_container_fixture import run


def verify(manifest, submission, output):
    if not submission.is_dir() or submission.is_symlink():
        raise ValueError("Submission must be a directory")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("id"), str) or not manifest["id"]:
        raise ValueError("Benchmark id required")
    image = manifest.get("image")
    if not isinstance(image, str) or not image:
        raise ValueError("Docker image required")
    checks = manifest.get("acceptance")
    if not isinstance(checks, dict):
        raise ValueError("Acceptance configuration required")
    command = checks.get("command")
    expected = checks.get("expected_files")
    if not isinstance(command, list) or not command:
        raise ValueError("Acceptance command required")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("Acceptance artifact digests required")
    definition = {
        "id": manifest["id"],
        "image": image,
        "command": command,
        "timeout_seconds": manifest.get("timeout_seconds", 60),
        "expected_files": expected,
    }
    result = run(definition, submission, output)
    result["evaluation_type"] = "independent-submission-verification"
    result["agent_identity"] = "unverified"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = verify(json.loads(args.manifest.read_text()), args.submission, args.output)
    print(json.dumps({"benchmark": result["benchmark"], "passed": result["passed"], "evidence": str(args.output)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
