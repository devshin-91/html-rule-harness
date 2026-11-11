"""Unit tests for schema_validator.py (Sub-task T2 verifier)."""

import unittest
from schema_validator import parse_quota_remaining, validate_task_spec


class TestSchemaValidator(unittest.TestCase):
    def test_valid_specs(self) -> None:
        ok, msg = validate_task_spec({"task_id": "t-1", "tier": "mid", "effort": "medium", "max_tokens": 512})
        self.assertTrue(ok, msg)
        self.assertEqual(msg, "ok")

    def test_reject_invalid_effort_typo(self) -> None:
        ok, _ = validate_task_spec({"task_id": "t-1", "tier": "mid", "effort": "med", "max_tokens": 512})
        self.assertFalse(ok)

    def test_reject_zero_or_bool_max_tokens(self) -> None:
        ok_zero, _ = validate_task_spec({"task_id": "t-1", "tier": "low", "effort": "low", "max_tokens": 0})
        self.assertFalse(ok_zero)
        ok_bool, _ = validate_task_spec({"task_id": "t-1", "tier": "low", "effort": "low", "max_tokens": True})
        self.assertFalse(ok_bool)

    def test_parse_quota_bounds(self) -> None:
        self.assertEqual(parse_quota_remaining("0%"), 0)
        self.assertEqual(parse_quota_remaining("95%"), 95)
        self.assertEqual(parse_quota_remaining("100%"), 100)
        with self.assertRaises(ValueError):
            parse_quota_remaining("105%")
        with self.assertRaises(ValueError):
            parse_quota_remaining("-5%")


if __name__ == "__main__":
    unittest.main()
