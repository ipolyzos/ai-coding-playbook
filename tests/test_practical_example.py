"""Check that the public practical fixture is executable and safe to onboard."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from aicp.__main__ import init, validate_config
from aicp.verification import verify

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "practical"


class PracticalExampleTests(unittest.TestCase):
    def test_fixture_onboarding_and_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "sample-service"
            shutil.copytree(FIXTURE, project)
            init(project, "codex")
            self.assertEqual(validate_config(project)["tool"], "codex")
            checks = json.loads((project / "checks.json").read_text(encoding="utf-8"))
            report = verify(project, project / "checks.json")
            self.assertTrue(report["passed"], report)
            self.assertEqual(len(report["checks"]), len(checks["checks"]))

    def test_sample_tests_directly(self):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=FIXTURE, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
