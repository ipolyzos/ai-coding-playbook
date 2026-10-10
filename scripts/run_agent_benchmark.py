#!/usr/bin/env python3
"""Opt-in orchestration of agent execution and independent Docker verification.

Only use on externally isolated disposable hosts. This is NOT a sandbox.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_agent_cli import run_agent
from scripts.verify_agent_submission import verify


def orchestrate(manifest, tool, argv, workspace, output_dir, timeout=300):
    if not isinstance(manifest, dict) or not isinstance(manifest.get("id"), str) or not manifest["id"]:
        raise ValueError("Manifest must have a nonempty id")
    if output_dir.exists() and (not output_dir.is_dir() or output_dir.is_symlink()):
        raise ValueError("Output must be a regular directory")
    # Refuse to store evidence in the mutable workspace or vice versa.
    workspace_path = workspace.resolve(strict=True)
    output_path = output_dir.resolve()
    if output_path == workspace_path or workspace_path in output_path.parents or output_path in workspace_path.parents:
        raise ValueError("Evidence directory must be separate from workspace")
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_path = output_dir / "execution.json"
    acceptance_path = output_dir / "acceptance.json"
    report_path = output_dir / "report.json"
    execution = run_agent(tool, argv, manifest["id"], workspace, execution_path, timeout)
    acceptance = None
    if execution["passed"]:
        acceptance = verify(manifest, workspace, acceptance_path)
    report = {
        "schema_version": 1,
        "benchmark": manifest["id"],
        "tool": tool,
        "agent_execution": execution,
        "acceptance": acceptance,
        "acceptance_attempted": acceptance is not None,
        "passed": bool(execution["passed"] and acceptance is not None and acceptance["passed"]),
        "security_boundary": "external-isolation-required",
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--tool", choices=["codex", "claude", "gemini"], required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv and args.argv[0] == "--" else args.argv
    report = orchestrate(json.loads(args.manifest.read_text(encoding="utf-8")), args.tool, argv, args.workspace, args.output_dir, args.timeout)
    print(json.dumps({"benchmark": report["benchmark"], "passed": report["passed"], "report": str(args.output_dir / "report.json")}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
