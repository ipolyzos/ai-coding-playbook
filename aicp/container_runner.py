"""Opt-in, constrained Docker runner for experimental agent commands.

This is defense in depth, not a hardened multi-tenant security boundary.
"""
import re


def docker_agent_command(project, image, argv):
    if not isinstance(image, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,253}", image):
        raise ValueError("Invalid container image reference")
    if not argv or not all(isinstance(arg, str) and arg for arg in argv):
        raise ValueError("Invalid agent argv")
    if not project.is_dir() or project.is_symlink():
        raise ValueError("Project must be an existing non-symlink directory")
    return [
        "docker", "run", "--rm", "--network", "none",
        "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", "128", "--memory", "1g", "--cpus", "1",
        "--user", "65534:65534",
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=64m",
        "--mount", "type=bind,src=" + str(project.resolve()) + ",dst=/workspace",
        "--workdir", "/workspace",
        image, *argv,
    ]
