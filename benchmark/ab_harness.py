#!/usr/bin/env python3
"""A/B Benchmark Harness with Resumable Checkpoint Cache (Arm A vs Arm B).

Arm A (Baseline):
  - Follows Google Harness² (`AGENTS.md` + `rules.md`) WITHOUT the HTML Branching Rule System.
  - Uses a fixed single model & effort for all sub-tasks: `gemini-4-argon-medium` (Gemini 4 Argon (Medium)).
  - Must load the un-routed full rule corpus (`55,577 B` / `~18,704 tokens`) when rule guidance is referenced.

Arm B (Treatment):
  - Follows Google Harness² + HTML Branching Rule System (`scripts/resolve_rule.py`).
  - Injects ONLY the single `<active_rule_packet>` (`~472-693 tokens`, 96.3%-97.5% context reduction).
  - Maps each sub-task's recommended `(tier, effort)` to the available Antigravity runtime models & efforts
    while respecting live quota guardrails:
      * T1 (`reasoning.simple-argument`, `low / low`) -> `gemini-4-argon-low`
      * T2 (`coding.quick-edit`, `low / low`) -> `gemini-4-argon-low`
      * T3 (`coding.debugging.runtime`, `mid / medium` or `mid / high` with verifier) -> `gemini-4-argon-medium`
      * T4 (`coding.debugging.concurrency`, `high / high`) -> `gemini-4-argon-high`

Resumable Checkpoint Cache:
  - Stored at `benchmark/cache/ab_checkpoint.json`.
  - Saves progress after every single sub-task so interrupted runs resume without losing completed tasks.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import shutil
import subprocess
import sys
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
BENCH_DIR = ROOT / "benchmark"
SEEDS_DIR = BENCH_DIR / "seeds"
CACHE_DIR = BENCH_DIR / "cache"
CHECKPOINT_PATH = CACHE_DIR / "ab_checkpoint.json"
PROMPTS_DIR = BENCH_DIR / "prompts"

SUBTASKS: List[Dict[str, Any]] = [
    {
        "id": "T1",
        "title": "쿼터 가드레일 정책 찬반 3줄 요약 및 경계 조건 논증",
        "task_query": "간단한 논증으로 에이전트 쿼터 가드레일(Rate-Limiter) 정책의 핵심 장단점 3줄 요약 및 성립 경계 조건 생성",
        "files": 1,
        "attempts": 0,
        "concurrency": False,
        "arm_a_model": "gemini-4-argon-medium",
        "arm_b_model": "gemini-4-argon-low",
        "target_file": "t1_policy_argument.md",
    },
    {
        "id": "T2",
        "title": "TaskSpec 및 QuotaBucket 스키마 검증기 빠른 코드 수정",
        "task_query": "단일 파일 schema_validator.py에서 TaskSpec 및 QuotaBucket 함수 빠른 수정 및 타이핑 오타 보완",
        "files": 1,
        "attempts": 0,
        "concurrency": False,
        "arm_a_model": "gemini-4-argon-medium",
        "arm_b_model": "gemini-4-argon-low",
        "target_file": "schema_validator.py",
    },
    {
        "id": "T3",
        "title": "task_queue.py 런타임 버그 3건 디버깅 및 단위/회귀 테스트",
        "task_query": "task_queue.py 런타임 오류 3건 디버깅 및 단위 테스트 통과",
        "files": 2,
        "attempts": 0,
        "concurrency": False,
        "arm_a_model": "gemini-4-argon-medium",
        "arm_b_model": "gemini-4-argon-medium",
        "target_file": "task_queue.py",
    },
    {
        "id": "T4",
        "title": "async_quota_pool.py 비동기 동시성 레이스 컨디션 디버깅 및 아키텍처 검증",
        "task_query": "async_quota_pool.py의 asyncio 비동기 동시성 레이스 컨디션 디버깅 및 스트레스 테스트 통과",
        "files": 4,
        "attempts": 1,
        "concurrency": True,
        "arm_a_model": "gemini-4-argon-medium",
        "arm_b_model": "gemini-4-argon-high",
        "target_file": "async_quota_pool.py",
    },
]


def load_checkpoint() -> Dict[str, Any]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if CHECKPOINT_PATH.exists():
        return json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    initial = {
        "benchmark_id": "harness2-html-rule-ab-v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "baseline_model": "gemini-4-argon-medium",
        "quota_snapshots": [],
        "arms": {
            "A": {"description": "Google Harness² Only (Fixed Gemini 4 Argon Medium, Un-routed Full Rules)", "tasks": {}},
            "B": {"description": "Google Harness² + HTML Branching Rule System (Dynamic Model/Effort + Active Rule Packet)", "tasks": {}},
        },
    }
    save_checkpoint(initial)
    return initial


def save_checkpoint(data: Dict[str, Any]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    CHECKPOINT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_full_unrouted_rules() -> str:
    """Concatenate all 27 HTML rule AI blocks to represent un-routed rule context in Arm A."""
    rules_dir = ROOT / "rules"
    html_files = [rules_dir / "router.html"] + sorted((rules_dir / "branches").rglob("*.html"))
    chunks: List[str] = []
    for p in html_files:
        rel = p.relative_to(ROOT).as_posix()
        chunks.append(f"<!-- FILE: {rel} -->\n" + p.read_text(encoding="utf-8"))
    return "\n\n".join(chunks)


def init_workspaces() -> None:
    """Initialize benchmark/workspace_a and benchmark/workspace_b from seeds and generate task packets."""
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    full_rules_dump = collect_full_unrouted_rules()
    (PROMPTS_DIR / "arm_a_full_rules_context.txt").write_text(full_rules_dump, encoding="utf-8")

    for arm in ("a", "b"):
        ws = BENCH_DIR / f"workspace_{arm}"
        ws.mkdir(parents=True, exist_ok=True)
        for seed_file in SEEDS_DIR.glob("*.py"):
            dest = ws / seed_file.name
            # Only copy seed if task not already completed in checkpoint
            ckpt = load_checkpoint()
            arm_tasks = ckpt["arms"][arm.upper()]["tasks"]
            if not arm_tasks:
                shutil.copy2(seed_file, dest)

    ckpt = load_checkpoint()
    for st in SUBTASKS:
        tid = st["id"]
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "resolve_rule.py"),
            "--task",
            st["task_query"],
            "--files",
            str(st["files"]),
            "--attempts",
            str(st["attempts"]),
            "--format",
            "json",
        ]
        if st["concurrency"]:
            cmd.append("--concurrency")
        out = subprocess.check_output(cmd, cwd=str(ROOT), text=True, encoding="utf-8")
        resolved = json.loads(out)
        (PROMPTS_DIR / f"arm_b_{tid.lower()}_packet.xml").write_text(resolved["packet_xml"], encoding="utf-8")
        (PROMPTS_DIR / f"arm_b_{tid.lower()}_resolved.json").write_text(
            json.dumps(resolved, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        for arm_key, model_slug in (("A", st["arm_a_model"]), ("B", st["arm_b_model"])):
            existing = ckpt["arms"][arm_key]["tasks"].get(tid, {})
            if existing.get("status") == "completed":
                continue
            ckpt["arms"][arm_key]["tasks"][tid] = {
                "id": tid,
                "title": st["title"],
                "status": "pending",
                "model_slug": model_slug,
                "branch": "unrouted_all_27_nodes" if arm_key == "A" else resolved["chain"][-1]["rule_id"],
                "recommended_tier": "mid (fixed)" if arm_key == "A" else resolved["recommendation"]["recommended_tier"],
                "recommended_effort": "medium (fixed)" if arm_key == "A" else resolved["recommendation"]["recommended_effort"],
                "decision_action": "fixed_baseline" if arm_key == "A" else resolved["recommendation"]["decision_action"],
                "rule_context_bytes": resolved["stats"]["total_tree_ai_bytes"] if arm_key == "A" else resolved["stats"]["packet_bytes"],
                "rule_context_tokens_est": resolved["stats"]["total_tree_tokens_est"] if arm_key == "A" else resolved["stats"]["packet_tokens_est"],
                "rule_context_saved_pct": 0.0 if arm_key == "A" else resolved["stats"]["saved_pct"],
            }
    save_checkpoint(ckpt)
    print(f"Initialized workspaces and checkpoint at {CHECKPOINT_PATH}")


def verify_workspace(arm: str) -> Dict[str, Any]:
    """Run automated verification & quality rubric (100 points total = 25 per subtask) on workspace_{a|b}."""
    ws = BENCH_DIR / f"workspace_{arm.lower()}"
    results: Dict[str, Any] = {}

    # T1 Verification (25 pts)
    t1_path = ws / "t1_policy_argument.md"
    t1_score = 0
    t1_notes: List[str] = []
    if t1_path.exists():
        text = t1_path.read_text(encoding="utf-8").strip()
        non_empty_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if any(k in text for k in ("전제", "장점", "찬성", "근거")) and any(k in text for k in ("결론", "단점", "한계", "경계")):
            t1_score += 10
            t1_notes.append("structure_ok(+10)")
        if 3 <= len(non_empty_lines) <= 12:
            t1_score += 10
            t1_notes.append(f"concise_lines={len(non_empty_lines)}(+10)")
        elif len(non_empty_lines) > 12:
            t1_score += 5
            t1_notes.append(f"verbose_lines={len(non_empty_lines)}(+5)")
        if any(k in text for k in ("경계", "한계", "예외", "독립", "5시간", "7일", "버킷", "조건")):
            t1_score += 5
            t1_notes.append("boundary_condition_ok(+5)")
    results["T1"] = {"score": t1_score, "max_score": 25, "passed": t1_score >= 20, "notes": t1_notes}

    # T2 Verification (25 pts)
    t2_score = 0
    t2_notes: List[str] = []
    p2 = subprocess.run(
        [sys.executable, "-m", "unittest", "test_schema_validator.py", "-v"],
        cwd=str(ws),
        capture_output=True,
        text=True,
    )
    if p2.returncode == 0:
        t2_score += 20
        t2_notes.append("unit_tests_passed(+20)")
    else:
        t2_notes.append("unit_tests_failed")
    sv_text = (ws / "schema_validator.py").read_text(encoding="utf-8") if (ws / "schema_validator.py").exists() else ""
    if '"""Validate a task specification dictionary.' in sv_text and '"""Parse a quota percentage string' in sv_text:
        t2_score += 5
        t2_notes.append("docstrings_preserved(+5)")
    results["T2"] = {"score": t2_score, "max_score": 25, "passed": p2.returncode == 0, "notes": t2_notes}

    # T3 Verification (25 pts)
    t3_score = 0
    t3_notes: List[str] = []
    p3 = subprocess.run(
        [sys.executable, "-m", "unittest", "test_task_queue.py", "-v"],
        cwd=str(ws),
        capture_output=True,
        text=True,
    )
    if p3.returncode == 0:
        t3_score += 18
        t3_notes.append("unit_tests_passed(+18)")
    tq_test_text = (ws / "test_task_queue.py").read_text(encoding="utf-8") if (ws / "test_task_queue.py").exists() else ""
    test_count = tq_test_text.count("def test_")
    if test_count >= 4:
        t3_score += 7
        t3_notes.append(f"added_regression_tests(count={test_count})(+7)")
    elif test_count == 3 and p3.returncode == 0:
        t3_score += 4
        t3_notes.append("base_tests_only(+4)")
    results["T3"] = {"score": t3_score, "max_score": 25, "passed": p3.returncode == 0, "notes": t3_notes}

    # T4 Verification (25 pts)
    t4_score = 0
    t4_notes: List[str] = []
    p4 = subprocess.run(
        [sys.executable, "-m", "unittest", "test_async_quota_pool.py", "-v"],
        cwd=str(ws),
        capture_output=True,
        text=True,
    )
    aq_text = (ws / "async_quota_pool.py").read_text(encoding="utf-8") if (ws / "async_quota_pool.py").exists() else ""
    if p4.returncode == 0:
        t4_score += 15
        t4_notes.append("concurrency_stress_passed(+15)")
    if "asyncio.Lock" in aq_text or "Lock(" in aq_text:
        t4_score += 5
        t4_notes.append("atomic_lock_used(+5)")
    t4_doc = ws / "t4_concurrency_notes.md"
    if t4_doc.exists() and "|" in t4_doc.read_text(encoding="utf-8"):
        t4_score += 5
        t4_notes.append("state_transition_table_documented(+5)")
    results["T4"] = {"score": t4_score, "max_score": 25, "passed": p4.returncode == 0, "notes": t4_notes}

    total_score = sum(v["score"] for v in results.values())
    return {"arm": arm.upper(), "total_score": total_score, "max_score": 100, "tasks": results}


def extract_transcript_telemetry(conv_id: str) -> Dict[str, Any]:
    """Read exact token counts and wall-clock timestamps from an Antigravity conversation transcript."""
    brain_dir = pathlib.Path.home() / ".gemini" / "antigravity" / "brain" / conv_id / ".system_generated" / "logs"
    t_path = brain_dir / "transcript.jsonl"
    if not t_path.exists():
        return {"error": f"transcript not found for {conv_id}"}

    input_tokens = 0
    cache_read_tokens = 0
    output_tokens = 0
    planner_steps = 0
    timestamps: List[dt.datetime] = []

    for line in t_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        ts_str = obj.get("created_at")
        if ts_str:
            timestamps.append(dt.datetime.fromisoformat(ts_str.replace("Z", "+00:00")))
        if obj.get("type") == "PLANNER_RESPONSE":
            planner_steps += 1
            input_tokens += int(obj.get("input_tokens", 0))
            cache_read_tokens += int(obj.get("cache_read_tokens", 0))
            output_tokens += int(obj.get("output_tokens", 0))

    elapsed_sec = 0.0
    if len(timestamps) >= 2:
        elapsed_sec = round((max(timestamps) - min(timestamps)).total_seconds(), 2)

    return {
        "conversation_id": conv_id,
        "planner_steps": planner_steps,
        "input_tokens": input_tokens,
        "cache_read_tokens": cache_read_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + cache_read_tokens + output_tokens,
        "active_tokens_non_cached": input_tokens + output_tokens,
        "elapsed_seconds": elapsed_sec,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="A/B Benchmark Harness")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p_ver = sub.add_parser("verify")
    p_ver.add_argument("--arm", choices=["A", "B", "all"], default="all")
    p_tel = sub.add_parser("telemetry")
    p_tel.add_argument("--conv-id", required=True)
    p_rec = sub.add_parser("record")
    p_rec.add_argument("--arm", choices=["A", "B"], required=True)
    p_rec.add_argument("--task", choices=["T1", "T2", "T3", "T4"], required=True)
    p_rec.add_argument("--conv-id", required=True)
    p_rec.add_argument("--wall-sec", type=float, default=0.0)

    args = parser.parse_args()
    if args.cmd == "init":
        init_workspaces()
    elif args.cmd == "verify":
        arms = ["A", "B"] if args.arm == "all" else [args.arm]
        out = {a: verify_workspace(a) for a in arms}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "telemetry":
        print(json.dumps(extract_transcript_telemetry(args.conv_id), ensure_ascii=False, indent=2))
    elif args.cmd == "record":
        ckpt = load_checkpoint()
        tel = extract_transcript_telemetry(args.conv_id)
        ver = verify_workspace(args.arm)["tasks"][args.task]
        entry = ckpt["arms"][args.arm]["tasks"].setdefault(args.task, {})
        entry["status"] = "completed" if ver["passed"] else "failed"
        entry["telemetry"] = tel
        if args.wall_sec > 0 and tel.get("elapsed_seconds", 0.0) == 0.0:
            entry["telemetry"]["elapsed_seconds"] = args.wall_sec
        entry["verification"] = ver
        save_checkpoint(ckpt)
        print(json.dumps(entry, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
