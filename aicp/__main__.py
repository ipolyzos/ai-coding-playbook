"""Dependency-free entry point: python3 -m aicp."""
import argparse
import json
from pathlib import Path
import shutil
import sys

from . import __version__
from .tasks import create_task
from .task_lifecycle import show_task, list_tasks
from .execution import run_task
from .verification import verify as run_verification
from .entrypoints import ENTRYPOINTS, install_entrypoint
from .planning import plan_init
from .inspection import inspect_project
from .adoption import adopt, plan_adoption
from .path_safety import require_safe_path, require_project

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("codex", "claude", "cursor", "copilot", "gemini")
CONFIG = ".aicp.json"


def validate_config(destination):
    require_project(destination)
    config_path = require_safe_path(destination, CONFIG)
    if not config_path.is_file():
        raise ValueError("Missing .aicp.json; run 'aicp init' first")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or config.get("schema_version") != 1 or config.get("tool") not in TOOLS:
        raise ValueError("Invalid playbook configuration")
    mode = config.get("mode", "init")
    expected = ".aicp/PLAYBOOK.md" if mode == "adopt" else "AGENTS.md"
    if mode not in ("init", "adopt") or config.get("instructions") != expected:
        raise ValueError("Invalid instruction file reference")
    instructions = require_safe_path(destination, expected)
    if not instructions.is_file():
        raise ValueError("Playbook instruction file is missing")
    if "AI Coding Playbook" not in instructions.read_text(encoding="utf-8"):
        raise ValueError("Playbook instruction file is invalid")
    if mode == "init" and ENTRYPOINTS[config["tool"]]:
        entrypoint = require_safe_path(destination, ENTRYPOINTS[config["tool"]])
        if not entrypoint.is_file():
            raise ValueError("Assistant-specific instruction entrypoint is missing")
    if mode == "adopt" and not inspect_project(destination)["existing_instructions"]:
        raise ValueError("Adopted repository is missing existing assistant instructions")
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
    preview = plan_init(destination, tool)
    if not preview["ready"]:
        raise FileExistsError("Initialization blocked: " + ", ".join(item["path"] for item in preview["files"] if item["action"] == "blocked"))
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
    try:
        install_entrypoint(destination, tool)
    except BaseException:
        config_path.unlink()
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
    init_parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    inspect_parser = commands.add_parser("inspect", help="Inventory existing assistant instructions")
    inspect_parser.add_argument("--path", type=Path, default=Path("."))
    adopt_parser = commands.add_parser("adopt", help="Prepare opt-in adoption without changing existing instructions")
    adopt_parser.add_argument("--tool", choices=TOOLS, required=True)
    adopt_parser.add_argument("--path", type=Path, default=Path("."))
    adopt_parser.add_argument("--dry-run", action="store_true")
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
    for action in ("validate", "show", "list"):
        command = task_commands.add_parser(action, help=action.capitalize() + " task drafts")
        command.add_argument("--path", type=Path, default=Path("."))
        if action != "list":
            command.add_argument("--name", required=True)
    run_parser = commands.add_parser("run", help="Run approved local agent and checks (not sandboxed)")
    run_parser.add_argument("--path", type=Path, default=Path("."))
    run_parser.add_argument("--name", required=True)
    run_parser.add_argument("--tool", choices=("codex", "claude", "gemini"), required=True)
    run_parser.add_argument("--checks", type=Path, required=True)
    run_parser.add_argument("--output", type=Path, required=True)
    run_parser.add_argument("--timeout", type=int, default=300)
    run_parser.add_argument("--container-image", help="Opt-in constrained Docker execution (no network)")
    run_parser.add_argument("--approve-host-execution", action="store_true", required=True)
    run_parser.add_argument("agent_argv", nargs=argparse.REMAINDER)
    verify_parser = commands.add_parser("verify", help="Run explicit project checks")
    verify_parser.add_argument("--path", type=Path, default=Path("."))
    verify_parser.add_argument("--checks", type=Path, required=True)
    verify_parser.add_argument("--output", type=Path, required=True)
    verify_parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            if args.dry_run:
                preview = plan_init(args.path, args.tool)
                print(json.dumps(preview, indent=2))
                return 0 if preview["ready"] else 1
            result = init(args.path, args.tool)
            print(f"Initialized {result}")
        elif args.command == "adopt":
            if args.dry_run:
                preview = plan_adoption(args.path, args.tool)
                print(json.dumps(preview, indent=2))
                return 0 if preview["ready"] else 1
            result = adopt(args.path, args.tool)
            print(f"Prepared optional playbook guidance: {result}")
            print("Manually review and reference .aicp/PLAYBOOK.md from existing instructions to enable it.")
        elif args.command == "inspect":
            print(json.dumps(inspect_project(args.path), indent=2))
        elif args.command == "verify":
            validate_config(args.path)
            result = run_verification(args.path, args.checks, args.timeout)
            if args.output.exists() or args.output.is_symlink():
                raise FileExistsError("Refusing to overwrite existing evidence")
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2)
                handle.write("\n")
            print(f"Verification {'passed' if result['passed'] else 'failed'}: {args.output}")
            summary = result["summary"]
            print(f"Checks: {summary['passed']}/{summary['total']} passed, {summary['timed_out']} timed out, {summary['launch_errors']} launch errors")
            for index, check in enumerate(result["checks"], 1):
                if not check["passed"]:
                    print(f"  Check {index}: {check['status']} (exit={check['exit_code']})")
            return 0 if result["passed"] else 1
        elif args.command == "run":
            validate_config(args.path)
            argv = args.agent_argv[1:] if args.agent_argv and args.agent_argv[0] == "--" else args.agent_argv
            report = run_task(args.path, args.name, args.tool, argv, args.checks, args.output, args.timeout, args.container_image)
            print(f"Execution {'passed' if report['passed'] else 'failed'}: {args.output}")
            return 0 if report["passed"] else 1
        elif args.command == "task":
            validate_config(args.path)
            if args.task_command == "create":
                result = create_task(args.path, args.name, args.objective, args.allow, args.accept)
                print(f"Created task {result}")
            elif args.task_command == "list":
                print(json.dumps({"tasks": list_tasks(args.path)}, indent=2))
            else:
                task = show_task(args.path, args.name)
                print(json.dumps(task if args.task_command == "show" else {"name": args.name, "valid": True}, indent=2))
        else:
            result = validate_config(args.path)
            print(f"Valid playbook configuration for {result['tool']}")
    except (ValueError, FileExistsError, OSError, json.JSONDecodeError) as exc:
        print(f"aicp: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
