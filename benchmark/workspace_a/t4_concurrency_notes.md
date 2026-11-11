# T4 Concurrency & Exception Rollback Notes (Arm A)

## State Transition & Synchronization
| State | Guard / Lock | Transition | Invariant |
|---|---|---|---|
| Check & Reserve | `self._lock` (`asyncio.Lock`) | Check `remaining_quota - cost >= min_reserve` and atomically decrement `remaining_quota -= cost` without yielding | `remaining_quota >= min_reserve` always holds |
| Execute Work | Unlocked during `await asyncio.sleep(0.001)` | Concurrent workers execute in parallel after reservation | Quota is already reserved |
| Commit | `self._lock` | Append `task_id` to `completed_tasks` | Task completion recorded |
| Rollback (Exception / CancelledError) | `BaseException` handler + `self._lock` | Restore `remaining_quota += cost` and append `task_id` to `rolled_back_tasks` before re-raising | Failed/cancelled tasks never leak quota |
