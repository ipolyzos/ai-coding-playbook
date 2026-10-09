"""Check restrictive Docker command construction without requiring Docker."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.run_container_fixture import run

from scripts.run_container_fixture import docker_argv


class DockerFixtureTests(unittest.TestCase):
    def test_restrictions_and_argv(self):
        with tempfile.TemporaryDirectory() as root:
            cmd = docker_argv("python:3.12-alpine", Path(root), ["python3", "-c", "print(1)"])
            for flag, value in [
                ("--network", "none"), ("--cap-drop", "ALL"),
                ("--security-opt", "no-new-privileges"),
                ("--pids-limit", "64"), ("--memory", "256m"),
                ("--user", "65534:65534"),
            ]:
                self.assertEqual(cmd[cmd.index(flag) + 1], value)
            self.assertIn("--read-only", cmd)
            self.assertEqual(cmd[-3:], ["python3", "-c", "print(1)"])

    def test_named_container(self):
        with tempfile.TemporaryDirectory() as root:
            cmd = docker_argv("python:3.12-alpine", Path(root), ["true"], "playbook-test")
            self.assertEqual(cmd[cmd.index("--name") + 1], "playbook-test")

    def test_cleanup_failure_blocks_pass(self):
        with tempfile.TemporaryDirectory() as root:
            base = Path(root)
            fixture = base / "fixture"
            fixture.mkdir()
            (fixture / "result.txt").write_bytes(b"ok")
            import hashlib
            definition = {"id": "test", "image": "python:3.12-alpine", "command": ["true"], "timeout_seconds": 5, "expected_files": {"result.txt": hashlib.sha256(b"ok").hexdigest()}}
            with patch("scripts.run_container_fixture.execute", return_value={"passed": True, "status": "completed"}), patch("scripts.run_container_fixture.subprocess.run", side_effect=OSError("daemon unavailable")):
                result = run(definition, fixture, base / "evidence.json")
            self.assertFalse(result["passed"])
            self.assertFalse(result["cleanup_succeeded"])

    def test_rejects_bad_image(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                docker_argv("bad image", Path(root), ["true"])

    def test_rejects_shell_string(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                docker_argv("python:3.12-alpine", Path(root), "echo hello")


if __name__ == "__main__":
    unittest.main()
