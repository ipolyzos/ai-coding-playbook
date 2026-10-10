import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.run_agent_benchmark import orchestrate


class AgentBenchmarkTests(unittest.TestCase):
    def test_runs_acceptance_after_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            with patch("scripts.run_agent_benchmark.run_agent", return_value={"passed": True}) as agent, patch("scripts.run_agent_benchmark.verify", return_value={"passed": True}) as acceptance:
                report = orchestrate({"id": "example"}, "codex", ["codex"], workspace, root / "evidence")
            self.assertTrue(report["passed"])
            self.assertTrue(report["acceptance_attempted"])
            self.assertTrue(agent.called)
            self.assertTrue(acceptance.called)
            self.assertEqual(report, json.loads((root / "evidence" / "report.json").read_text()))

    def test_skips_acceptance_when_agent_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            with patch("scripts.run_agent_benchmark.run_agent", return_value={"passed": False}), patch("scripts.run_agent_benchmark.verify") as acceptance:
                report = orchestrate({"id": "example"}, "codex", ["codex"], workspace, root / "evidence")
            self.assertFalse(report["passed"])
            self.assertFalse(report["acceptance_attempted"])
            acceptance.assert_not_called()

    def test_refuses_evidence_inside_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            with self.assertRaises(ValueError):
                orchestrate({"id": "example"}, "codex", ["codex"], workspace, workspace / "evidence")


if __name__ == "__main__":
    unittest.main()
