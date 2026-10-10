"""Dependency-free entry point: python3 -m aicp."""
import argparse
import json
from pathlib import Path
import shutil
import sys

from . import __version__
from .tasks import create_task
from .verification import verify as run_verification

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("codex", "claude", "cursor", "copilot", "gemini")
CONFIG = ".aicp.json"


def validate_config(destination):
    config_path = destination / CONFIG
    if not config_path.is_file() or config_path.is_symlink():
        raise ValueError("Missing .aicp.json; run 'aicp init' first")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or config.get("schema_version") != 1 or config.get("tool") not in TOOLS:
        raise ValueError("Invalid playbook configuration")
    if config.get("instructions") != "AGENTS.md":
        raise ValueError("Invalid instruction file reference")
    instructions = destination / "AGENTS.md"
    if not instructions.is_file() or instructions.is_symlink():
        raise ValueError("AGENTS.md is missing or is a symlink")
    if "AI Coding Playbook" not in instructions.read_text(encoding="utf-8"):
        raise ValueError("AGENTS.md does not contain playbook instructions")
    return config


def init(destination, tool):
    if tool not in TOOLS:
        raise ValueError("Unsupported tool")
    if not destination.is_dir() or destination.is_symlink():
        raise ValueError("Target must be an existing directory")
    config_path = destination / CONFIG
    instructions = destination / "AGENTS.md"
    if config_path.exists() or config_path.is_symlink() or instructions.exists() or instructions.is_symlink():
        raise FileExistsError("Refusing to overwrite .aicp.json or AGENTS.md")
    content = (
        "# AI Coding Playbook — repository instructions\n\n"
        "Use engineering standards: small scoped changes, explicit acceptance criteria, "
        "relevant tests, and truthful verification reports. Never claim a check passed "
        "without evidence. Require approval for destructive actions, credential access, "
        "deployments, and permission changes. Keep all changes in reviewed feature branches.\n\n"
        "This generated file is a starting point. Customize it for your repository. "
        "See https://github.com/ipolyzos/ai-coding-playbook for the full prompt library.\n"
    )
    # Exclusive creation avoids accidental overwrites and follows a fail-closed policy.
    with instructions.open("x", encoding="utf-8") as handle:
        handle.write(content)
    try:
        with config_path.open("x", encoding="utf-8") as handle:
            json.dump({"schema_version": 1, "tool": tool, "instructions": "AGENTS.md"}, handle, indent=2)
            handle.write("\n")
    except BaseException:
        instructions.unlink()
        raise
    return config_path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aicp")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    init_parser = commands.add_parser("init", help="Initialize a repository")
    init_parser.add_argument("--tool", choices=TOOLS, required=True)
    init_parser.add_argument("--path", type=Path, default=Path("."))
    check_parser = commands.add_parser("validate", help="Validate repository setup")
    check_parser.add_argument("--path", type=Path, default=Path("."))
    task_parser = commands.add_parser("task", help="Manage engineering task drafts")
    task_commands = task_parser.add_subparsers(dest="task_command", required=True)
    create_parser = task_commands.add_parser("create", help="Create a structured task")
    create_parser.add_argument("--path", type=Path, default=Path("."))
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--objective", required=True)
    create_parser.add_argument("--allow", action="append", required=True)
    create_parser.add_argument("--accept", action="append", required=True)
    verify_parser = commands.add_parser("verify", help="Run explicit project checks")
    verify_parser.add_argument("--path", type=Path, default=Path("."))
    verify_parser.add_argument("--checks", type=Path, required=True)
    verify_parser.add_argument("--output", type=Path, required=True)
    verify_parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init(args.path, args.tool)
            print(f"Initialized {result}")
        elif args.command == "verify":
            validate_config(args.path)
            result = run_verification(args.path, args.checks, args.timeout)
            if args.output.exists() or args.output.is_symlink():
                raise FileExistsError("Refusing to overwrite existing evidence")
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2)
                handle.write("\\n")
            print(f"Verification {'passed' if result['passed'] else 'failed'}: {args.output}")
            return 0 if result["passed"] else 1
        elif args.command == "task":
            validate_config(args.path)
            result = create_task(args.path, args.name, args.objective, args.allow, args.accept)
            print(f"Created task {result}")
        else:
            result = validate_config(args.path)
            print(f"Valid playbook configuration for {result['tool']}")
    except (ValueError, FileExistsError, OSError, json.JSONDecodeError) as exc:
        print(f"aicp: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
