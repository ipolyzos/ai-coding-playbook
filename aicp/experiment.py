"""Validate experimental benchmark manifests without running agents."""
import json
from pathlib import Path

CONDITIONS = ("baseline", "playbook")
REQUIRED = {"schema_version", "experiment_id", "agent", "fixture_revision", "tasks", "repetitions", "timeout_seconds"}


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != REQUIRED or manifest["schema_version"] != 1:
        raise ValueError("Invalid experimental manifest fields")
    for key in ("experiment_id", "agent", "fixture_revision"):
        if not isinstance(manifest[key], str) or not manifest[key].strip():
            raise ValueError("Missing experiment metadata: " + key)
    if type(manifest["repetitions"]) is not int or not 1 <= manifest["repetitions"] <= 100:
        raise ValueError("Repetitions must be between 1 and 100")
    if type(manifest["timeout_seconds"]) is not int or not 1 <= manifest["timeout_seconds"] <= 3600:
        raise ValueError("Timeout must be between 1 and 3600 seconds")
    tasks = manifest["tasks"]
    if not isinstance(tasks, list) or not tasks or len(tasks) > 100 or any(
        not isinstance(t, str) or not t.strip() for t in tasks
    ) or len(set(tasks)) != len(tasks):
        raise ValueError("Tasks must be a nonempty unique list")
    return manifest


def load_manifest(path):
    if not isinstance(path, Path):
        path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError("Manifest must be a regular file")
    return validate_manifest(json.loads(path.read_text(encoding="utf-8")))
