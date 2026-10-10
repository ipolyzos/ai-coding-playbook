"""Scope auditing unit tests."""
import unittest
from aicp.scope_audit import audit_scope


class ScopeAuditTests(unittest.TestCase):
    def test_prefixes_are_directory_boundaries(self):
        result = audit_scope(set(), {"src/a.py", "src-extra/b.py", "tests/test_a.py"}, ["src/", "tests/"])
        self.assertEqual(result["outside_allowed_paths"], ["src-extra/b.py"])
        self.assertFalse(result["passed"])

    def test_exact_file_allowed(self):
        result = audit_scope(set(), {"README.md"}, ["README.md"])
        self.assertTrue(result["passed"])

    def test_clean_delta(self):
        result = audit_scope(set(), set(), ["src/"])
        self.assertTrue(result["passed"])


if __name__ == "__main__":
    unittest.main()
