"""Constrained Docker command tests (no Docker daemon required)."""
from pathlib import Path
import tempfile
import unittest

from aicp.container_runner import docker_agent_command


class ContainerRunnerTests(unittest.TestCase):
    def test_constrained_flags_and_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = docker_agent_command(Path(tmp), "example/agent:local", ["codex", "exec", "task"])
        self.assertEqual(command[:3], ["docker", "run", "--rm"])
        self.assertIn("none", command)
        self.assertIn("--cap-drop", command)
        self.assertIn("no-new-privileges", command)
        self.assertIn("--read-only", command)
        self.assertEqual(command[-4:], ["example/agent:local", "codex", "exec", "task"])

    def test_invalid_image_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                docker_agent_command(Path(tmp), "--privileged", ["codex"])

    def test_symlink_project_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "repo").mkdir()
            (root / "link").symlink_to(root / "repo", target_is_directory=True)
            with self.assertRaises(ValueError):
                docker_agent_command(root / "link", "agent:latest", ["codex"])


if __name__ == "__main__":
    unittest.main()
