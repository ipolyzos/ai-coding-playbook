#!/usr/bin/env python3
"""Run a trusted benchmark in a disposable copy and verify expected artifacts.

Temporary directories isolate fixture changes from the source tree, but do not
provide an OS security sandbox. Do not run untrusted agent code with this runner.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_benchmark import execute


def run_fixture(definition, fixture, output):
    if not fixture.is_dir():
        raise ValueError("Fixture directory does not exist")
    expected = definition.get("expected_files")
    if not isinstance(expected, dict) or not expected:
        raise ValueError("expected_files must be a nonempty path-to-sha256 mapping")
    for path, digest in expected.items():
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts or not path or not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("Invalid expected artifact path or digest")
    if any(p.is_symlink() for p in fixture.rglob("*")):
        raise ValueError("Fixture contains symlinks")
    with tempfile.TemporaryDirectory(prefix="playbook-fixture-") as temporary:
        workspace = Path(temporary) / "workspace"
        shutil.copytree(fixture, workspace, symlinks=False)
        # Never follow symlinks from fixture files or generated artifacts.
        if any(p.is_symlink() for p in workspace.rglob("*")):
            raise ValueError("Fixture contains symlinks")
        execution = execute(definition, workspace, output)
        assertions = {}
        for relative, digest in expected.items():
            candidate = workspace / relative
            if not candidate.is_file() or candidate.is_symlink():
                assertions[relative] = False
            else:
                assertions[relative] = hashlib.sha256(candidate.read_bytes()).hexdigest() == digest
        result = {
            **execution,
            "fixture": str(fixture.resolve()),
            "assertions": assertions,
            "passed": execution["passed"] and all(assertions.values()),
        }
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("definition", type=Path)
    parser.add_argument("--fixture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    definition = json.loads(args.definition.read_text(encoding="utf-8"))
    result = run_fixture(definition, args.fixture, args.output)
    print(json.dumps({"benchmark": result["benchmark"], "passed": result["passed"], "assertions": result["assertions"], "evidence": str(args.output)}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
