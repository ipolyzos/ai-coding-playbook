"""Deterministic tests for the public documentation fixture."""
import unittest

from sample_service import health, retry


class SampleServiceTests(unittest.TestCase):
    def test_retry_recovers(self):
        calls = []

        def flaky():
            calls.append(1)
            if len(calls) < 3:
                raise ValueError("temporary")
            return "ok"

        self.assertEqual(retry(flaky), "ok")
        self.assertEqual(len(calls), 3)

    def test_retry_exhaustion(self):
        with self.assertRaisesRegex(ValueError, "temporary"):
            retry(lambda: (_ for _ in ()).throw(ValueError("temporary")), attempts=2)

    def test_retry_rejects_zero_attempts(self):
        with self.assertRaises(ValueError):
            retry(lambda: "ok", attempts=0)

    def test_health(self):
        self.assertEqual(health(), (200, {"status": "ok"}))


if __name__ == "__main__":
    unittest.main()
