# T4 Concurrency Debugging Notes (`coding.debugging.concurrency`)

## 1. State Transition, Lock Acquisition Order & Async Cancellation/Timeout Boundaries

Following `<active_rule_packet>` (`coding.debugging.concurrency`), the state transitions, lock ordering, and async yield/cancellation boundaries for [`AsyncQuotaPool.allocate_and_run`](./benchmark/workspace_b/async_quota_pool.py) are mapped below before applying deterministic synchronization:

| State / Phase | Pre-Condition | Lock Order (`self._lock`) | Async Yield / Timeout / Cancellation Boundary | State Transition & Post-Condition | Exception / Rollback Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0. Validate** | `cost > 0` checked | None (stateless check) | None (synchronous) | `cost <= 0` -> raises `ValueError`; otherwise proceed to **Reserve** | Immediate `ValueError`, no state mutated |
| **1. Reserve / Reject** | `IDLE -> RESERVING` | Acquire `self._lock` (Order #1, single pool lock) | `await asyncio.sleep(0)` inside critical section protected by `self._lock` | If `remaining_quota - cost < min_reserve`: append `task_id` to `rejected_tasks`, transition to `REJECTED` (`False`). Else: `remaining_quota -= cost`, transition to `RESERVED` | If cancelled before lock acquisition or before deduction, `remaining_quota` is unchanged |
| **2. Execute Worker** | `RESERVED -> EXECUTING` | Release `self._lock` during worker I/O | `await asyncio.sleep(0.001)` (worker coroutine execution boundary; cancellation or failure may occur here) | On normal completion (`simulate_fail=False`), proceed to **Commit**; on failure/cancellation, enter **Rollback** | Any `BaseException` (`RuntimeError`, `asyncio.CancelledError`, `TimeoutError`) triggers **Rollback** |
| **3. Commit** | `EXECUTING -> COMMITTED` | Acquire `self._lock` (Order #1) | None inside lock body | Append `task_id` to `completed_tasks`, return `True` (`remaining_quota` keeps deducted value) | None |
| **4. Rollback** | `EXECUTING -> ROLLED_BACK` | Acquire `self._lock` (Order #1) | Entering `except BaseException:` handler after worker failure/cancellation | Restore `remaining_quota += cost`, append `task_id` to `rolled_back_tasks`, re-raise exception | Quota invariant `remaining_quota >= min_reserve` and total usable pool capacity are deterministically restored |

## 2. Root Cause & Deterministic Fix

1. **Check-Then-Act Race Across `await` (Bug 1)**: `remaining_quota - cost < min_reserve` and `remaining_quota -= cost` were separated by `await asyncio.sleep(0)` without synchronization, allowing 50 concurrent coroutines to pass the guard simultaneously and overspend quota below `min_reserve`. Fixed by serializing the check-and-deduct critical section with `self._lock = asyncio.Lock()`.
2. **Missing Quota Rollback on Worker Failure/Cancellation (Bug 2)**: When worker execution raised `RuntimeError` (or `BaseException` including cancellation), `task_id` was appended to `rolled_back_tasks` without restoring `self.remaining_quota += cost`. Fixed by atomically restoring `self.remaining_quota += cost` and recording `self.rolled_back_tasks.append(task_id)` under `self._lock` before re-raising.
