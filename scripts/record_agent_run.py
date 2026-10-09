#!/usr/bin/env python3
"""Record a manually launched coding-agent run without claiming verified identity.

This script records declared tool metadata, a local workspace fingerprint and
a transcript hash. It never executes agents or reads secrets from the transcript
into its output. Provenance is self-declared until independently attested.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sys


def fingerprint(directory):
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError("Workspace must be a directory")
    files = []
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError("Workspace symlinks are not supported")
        if path.is_file():
            relative = path.relative_to(directory).as_posix()
            files.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    canonical = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest(), len(files)


def record(agent, version, task, workspace, transcript, output):
    if not all(isinstance(v, str) and v.strip() for v in (agent, version, task)):
        raise ValueError("Agent, version and task must be nonempty")
    if not transcript.is_file() or transcript.is_symlink():
        raise ValueError("Transcript must be a regular file")
    digest, count = fingerprint(workspace)
    evidence = {
        "schema_version": 1,
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "agent_declared": agent,
        "version_declared": version,
        "task": task,
        "identity_verification": "self-declared",
        "workspace_sha256": digest,
        "workspace_file_count": count,
        "transcript_sha256": hashlib.sha256(transcript.read_bytes()).hexdigest(),
        "transcript_bytes": transcript.stat().st_size,
        "execution_verified": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = record(args.agent, args.version, args.task, args.workspace, args.transcript, args.output)
    print(json.dumps({"task": result["task"], "workspace_sha256": result["workspace_sha256"], "evidence": str(args.output)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
