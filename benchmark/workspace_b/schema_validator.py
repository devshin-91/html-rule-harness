"""Schema validator for Agent Task Queue & Quota Guardrail Engine (Sub-task T2 seed)."""

from typing import Any, Dict, Tuple

VALID_TIERS = ("low", "mid", "high")
# BUG 1: "medium" is missing from VALID_EFFORTS (has typo "med" instead of "medium")
VALID_EFFORTS = ("low", "medium", "high")


def validate_task_spec(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate a task specification dictionary.

    Required keys:
      - task_id (non-empty str)
      - tier (one of: "low", "mid", "high")
      - effort (one of: "low", "medium", "high")
      - max_tokens (positive int > 0)
    Returns (is_valid, error_message).
    """
    if not isinstance(spec, dict):
        return False, "spec must be a dict"

    task_id = spec.get("task_id")
    if not isinstance(task_id, str) or not task_id.strip():
        return False, "invalid task_id"

    tier = spec.get("tier")
    if tier not in VALID_TIERS:
        return False, f"invalid tier: {tier}"

    effort = spec.get("effort")
    if effort not in VALID_EFFORTS:
        return False, f"invalid effort: {effort}"

    max_tokens = spec.get("max_tokens")
    # BUG 2: bool is a subclass of int in Python (isinstance(True, int) is True),
    # and max_tokens == 0 is wrongly allowed (should require > 0 and not bool).
    if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens <= 0:
        return False, "invalid max_tokens"

    return True, "ok"


def parse_quota_remaining(quota_str: str) -> int:
    """Parse a quota percentage string like '95%' into an integer 0..100.

    Raises ValueError if format is invalid or value is outside 0..100.
    """
    if not isinstance(quota_str, str) or not quota_str.endswith("%"):
        raise ValueError("quota_str must end with '%'")
    raw = quota_str[:-1].strip()
    if not raw.isdigit():
        raise ValueError("quota_str must contain non-negative integer percentage")
    val = int(raw)
    # BUG 3: missing upper-bound check for val > 100
    if val > 100:
        raise ValueError("quota_str percentage must be <= 100")
    return val
