#!/usr/bin/env python3
"""Deep Quality & Effectiveness Audit of Arm A vs Arm B (Gemini 4 Argon High Inspector).

Evaluates both workspaces across 6 strict engineering & rule-adherence dimensions:
  1. Functional Correctness (Seeded unit & concurrency stress tests)
  2. Adversarial Edge-Case Resilience (Task cancellation via asyncio.CancelledError, caller list mutation, whitespace/type edge cases)
  3. Comment & Docstring Integrity (`coding.root` rule: preserve all existing comments and docstrings)
  4. Concurrency Yield-Point Fidelity (Preserving `await asyncio.sleep(0)` inside `async with self._lock:` to prove lock serialization across event-loop yields)
  5. Cross-Branch Context Bleed vs. Focus (`T1` overthinking/bleed check, `T3` boundary regression test addition, `T4` 6-column state-transition/lock/cancellation table)
  6. Token & Cost-Effectiveness Ratio (Quality points achieved per 10,000 tokens consumed)
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import pathlib
import sys
from typing import Any, Dict

ROOT = pathlib.Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmark"
SEEDS_DIR = BENCH_DIR / "seeds"
CKPT_PATH = BENCH_DIR / "cache" / "ab_checkpoint.json"


def load_module(mod_name: str, file_path: pathlib.Path) -> Any:
    spec = importlib.util.spec_from_file_location(mod_name, str(file_path))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


def audit_arm(arm: str) -> Dict[str, Any]:
    ws = BENCH_DIR / f"workspace_{arm.lower()}"
    report: Dict[str, Any] = {"arm": arm.upper(), "subtasks": {}}

    # --- T1 Audit (25 pts strict high-effort rubric) ---
    t1_text = (ws / "t1_policy_argument.md").read_text(encoding="utf-8")
    t1_lines = [ln.strip() for ln in t1_text.splitlines() if ln.strip()]
    bleed_terms = ["PreToolUse", "Swarm/Graph", "Context Rot", "Unbounded Retry Loop"]
    found_bleed = [t for t in bleed_terms if t in t1_text]
    t1_score = 0
    # 1) Required 4-part logical progression (8 pts)
    if all(any(k in t1_text for k in grp) for grp in [("전제",), ("근거", "장점", "장단점"), ("결론",), ("한계", "경계")]):
        t1_score += 8
    # 2) Conciseness & Overthinking Guard (8 pts: <=8 lines gets 8, >12 lines gets 2)
    if len(t1_lines) <= 8:
        t1_score += 8
    elif len(t1_lines) <= 12:
        t1_score += 5
    else:
        t1_score += 2
    # 3) Zero Cross-Branch Context Bleed (5 pts)
    if not found_bleed:
        t1_score += 5
    # 4) Explicit 5-hour vs 7-day bucket separation boundary condition (4 pts)
    if "5시간" in t1_text and "7일" in t1_text:
        t1_score += 4

    report["subtasks"]["T1"] = {
        "strict_score": t1_score,
        "max_score": 25,
        "non_empty_lines": len(t1_lines),
        "char_count": len(t1_text),
        "cross_branch_bleed_terms": found_bleed,
    }

    # --- T2 Audit (25 pts strict high-effort rubric) ---
    sv_path = ws / "schema_validator.py"
    sv_text = sv_path.read_text(encoding="utf-8")
    sv_mod = load_module(f"sv_{arm}", sv_path)
    t2_checks = [
        sv_mod.validate_task_spec({"task_id": "x", "tier": "low", "effort": "medium", "max_tokens": 1}) == (True, "ok"),
        sv_mod.validate_task_spec({"task_id": "x", "tier": "low", "effort": "med", "max_tokens": 1})[0] is False,
        sv_mod.validate_task_spec({"task_id": "x", "tier": "low", "effort": "low", "max_tokens": True})[0] is False,
        sv_mod.validate_task_spec({"task_id": "x", "tier": "low", "effort": "low", "max_tokens": 0})[0] is False,
        sv_mod.parse_quota_remaining(" 100%") == 100,
    ]
    try:
        sv_mod.parse_quota_remaining("101%")
        t2_checks.append(False)
    except ValueError:
        t2_checks.append(True)

    t2_comments_kept = all(tag in sv_text for tag in ("# BUG 1:", "# BUG 2:", "# BUG 3:"))
    t2_score = (20 if all(t2_checks) else 0) + (5 if t2_comments_kept else 0)
    report["subtasks"]["T2"] = {
        "strict_score": t2_score,
        "max_score": 25,
        "adversarial_checks_passed": f"{sum(t2_checks)}/{len(t2_checks)}",
        "comments_and_docstrings_preserved": t2_comments_kept,
    }

    # --- T3 Audit (25 pts strict high-effort rubric) ---
    tq_path = ws / "task_queue.py"
    tq_test_path = ws / "test_task_queue.py"
    tq_text = tq_path.read_text(encoding="utf-8")
    tq_test_text = tq_test_path.read_text(encoding="utf-8")
    tq_mod = load_module(f"tq_{arm}", tq_path)

    # Check caller-list mutation isolation & zero-retry boundary
    caller_list = ["a"]
    q_inst = tq_mod.TaskQueue(caller_list)
    caller_list.append("b")
    caller_isolated = q_inst.tags == ["a"]
    q_inst.enqueue("z", "p", max_retries=0)
    zero_retry_ok = q_inst.record_failure("z") == "failed"
    t3_comments_kept = all(tag in tq_text for tag in ("# BUG 1:", "# BUG 2:", "# BUG 3:"))
    test_methods_count = tq_test_text.count("def test_")

    t3_score = 0
    if caller_isolated and zero_retry_ok:
        t3_score += 15
    if t3_comments_kept:
        t3_score += 3
    if test_methods_count >= 4:
        t3_score += 7  # Explicitly followed coding.debugging.runtime regression test rule

    report["subtasks"]["T3"] = {
        "strict_score": t3_score,
        "max_score": 25,
        "caller_list_mutation_isolated": caller_isolated,
        "zero_retry_boundary_ok": zero_retry_ok,
        "comments_preserved": t3_comments_kept,
        "unit_test_methods_count": test_methods_count,
        "regression_test_added": test_methods_count >= 4,
    }

    # --- T4 Audit (25 pts strict high-effort rubric) ---
    aq_path = ws / "async_quota_pool.py"
    aq_text = aq_path.read_text(encoding="utf-8")
    aq_mod = load_module(f"aq_{arm}", aq_path)
    notes_path = ws / "t4_concurrency_notes.md"
    notes_text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""

    # Adversarial mid-execution asyncio.CancelledError rollback test
    async def test_cancellation_rollback() -> bool:
        pool = aq_mod.AsyncQuotaPool(initial_quota=30, min_reserve=5)
        tasks = [asyncio.create_task(pool.allocate_and_run(f"c-{i}", cost=5)) for i in range(4)]
        await asyncio.sleep(0.0002)  # Let tasks reserve quota and enter worker sleep(0.001)
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        return pool.remaining_quota == 30 and len(pool.rolled_back_tasks) == 4

    cancel_ok = asyncio.run(test_cancellation_rollback())
    t4_comments_kept = "# BUG 1 (Race Condition):" in aq_text and "# BUG 2: Missing quota rollback" in aq_text
    yield_kept_in_lock = "await asyncio.sleep(0)" in aq_text
    detailed_table = notes_text.count("|") >= 30 and "Lock Order" in notes_text and "Cancellation" in notes_text

    t4_score = 0
    if cancel_ok:
        t4_score += 12
    if t4_comments_kept:
        t4_score += 4  # coding.root: preserve existing comments
    if yield_kept_in_lock:
        t4_score += 4  # coding.debugging.concurrency: preserve yield test condition inside lock
    if detailed_table:
        t4_score += 5  # coding.debugging.concurrency: full state-transition + lock order + cancellation table
    elif "|" in notes_text:
        t4_score += 2

    report["subtasks"]["T4"] = {
        "strict_score": t4_score,
        "max_score": 25,
        "cancelled_error_rollback_passed": cancel_ok,
        "seed_comments_preserved": t4_comments_kept,
        "context_switch_yield_preserved_in_lock": yield_kept_in_lock,
        "full_state_lock_cancellation_table": detailed_table,
    }

    report["strict_total_score"] = sum(v["strict_score"] for v in report["subtasks"].values())
    return report


def main() -> None:
    ckpt = json.loads(CKPT_PATH.read_text(encoding="utf-8"))
    res_a = audit_arm("A")
    res_b = audit_arm("B")

    for arm_key, res in (("A", res_a), ("B", res_b)):
        tot_tok = ckpt["arms"][arm_key]["summary"]["total_tokens"]
        inp_tok = ckpt["arms"][arm_key]["summary"]["input_tokens_total"]
        res["total_tokens"] = tot_tok
        res["input_tokens"] = inp_tok
        res["strict_score_per_10k_total_tokens"] = round(res["strict_total_score"] / (tot_tok / 10000.0), 2)
        res["strict_score_per_10k_input_tokens"] = round(res["strict_total_score"] / (inp_tok / 10000.0), 2)

    out = {"inspector_model": "Gemini 4 Argon (High)", "A": res_a, "B": res_b}
    out_path = BENCH_DIR / "cache" / "high_effort_quality_audit.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
