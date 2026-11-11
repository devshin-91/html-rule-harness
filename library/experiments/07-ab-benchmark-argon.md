# Iteration 07 — Real A/B Benchmark on Gemini 4 Argon (Arm A Baseline vs Arm B HTML Rule System)

## Goal
Empirically evaluate the effectiveness of the HTML Branching Rule System + Dynamic Model/Effort Routing (Arm B) against a pure Google Harness² baseline using fixed `Gemini 4 Argon (Medium)` and un-routed full rules (Arm A), with resumable checkpoint caching (`benchmark/cache/ab_checkpoint.json`).

## Design
- **Composite Engineering Task**: Build and verify an Agent Task Queue & Quota Guardrail Engine across 4 sub-tasks:
  - `T1`: Policy pros/cons 3-line summary & boundary condition (`reasoning.simple-argument`, `low / low`)
  - `T2`: `schema_validator.py` quick edit & validation (`coding.quick-edit`, `low / low`)
  - `T3`: `task_queue.py` 3 runtime bugs + unit/regression tests (`coding.debugging.runtime`, `mid / medium`)
  - `T4`: `async_quota_pool.py` async race condition & rollback + state-transition table (`coding.debugging.concurrency`, `high / high`)
- **Arm A (Baseline)**: All 4 sub-tasks run on `gemini-4-argon-medium` with the un-routed rule corpus (`18,704 tok` / task).
- **Arm B (Treatment)**: Sub-tasks routed via `scripts/resolve_rule.py` (`472–689 tok` packet, saving `96.3%–97.5%` rule context) and mapped to `gemini-4-argon-low` (T1, T2), `gemini-4-argon-medium` (T3), and `gemini-4-argon-high` (T4).

## Results
- **Input Tokens**: Arm A `129,114` vs Arm B `85,309` (**-33.9% / -43,805 tokens**)
- **Cache Read Tokens**: Arm A `266,691` vs Arm B `180,312` (**-32.4% / -86,379 tokens**)
- **Total Tokens**: Arm A `402,239` vs Arm B `276,264` (**-31.3% / -125,975 tokens**)
- **T1 Latency & Output**: Arm B (`gemini-4-argon-low` + `reasoning.simple-argument`) finished in `17.0s` vs `27.0s` (**-37.0%**) and used `565` vs `1,431` output tokens (**-60.5%**).
- **Quality / Verification Score**: Arm B scored **`100 / 100`** vs Arm A **`92 / 100`** (`+8.0 pts`), as Arm B followed the focused rule packet to add boundary regression tests in T3 and preserve existing comments + document the 5-phase lock/cancellation table in T4.
- **Quota Bucket Finding**: `gemini-4-argon-{low,medium,high}` uses a 7-day weekly quota bucket (`resets: 2026-11-18T21:35:25Z`), separate from `gemini-3.8-flash`'s 5-hour rolling bucket; all 8 Argon benchmark workers (`678,503` total tokens combined) consumed only `2%p` (`95% -> 93%`) of the Argon weekly quota.
