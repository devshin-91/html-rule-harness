"""Async Quota Reservation Pool with seeded concurrency race condition (Sub-task T4 seed)."""

import asyncio
from typing import Dict, List


class AsyncQuotaPool:
    """Manages concurrent quota reservations across async agent workers.

    Invariants required:
      1. `remaining_quota` must NEVER drop below `min_reserve` (default 5).
      2. Concurrent `allocate_and_run` calls must be serialized atomically during
         reservation/commit/rollback so that check-then-act races across `await`
         boundaries cannot double-spend quota.
      3. If `worker_coro` raises an exception or is cancelled after reservation,
         the reserved quota units must be rolled back (restored) cleanly.
    """

    def __init__(self, initial_quota: int = 100, min_reserve: int = 5) -> None:
        self.initial_quota = initial_quota
        self.remaining_quota = initial_quota
        self.min_reserve = min_reserve
        self._lock = asyncio.Lock()
        self.completed_tasks: List[str] = []
        self.rejected_tasks: List[str] = []
        self.rolled_back_tasks: List[str] = []

    async def allocate_and_run(self, task_id: str, cost: int, simulate_fail: bool = False) -> bool:
        """Reserve `cost` quota units if `remaining_quota - cost >= min_reserve`, execute work, and commit.

        Returns True if executed and committed, False if rejected due to insufficient quota.
        """
        if cost <= 0:
            raise ValueError("cost must be positive")

        async with self._lock:
            if self.remaining_quota - cost < self.min_reserve:
                self.rejected_tasks.append(task_id)
                return False
            self.remaining_quota -= cost

        try:
            await asyncio.sleep(0.001)
            if simulate_fail:
                raise RuntimeError(f"Simulated worker failure in {task_id}")
            async with self._lock:
                self.completed_tasks.append(task_id)
            return True
        except BaseException:
            async with self._lock:
                self.remaining_quota += cost
                self.rolled_back_tasks.append(task_id)
            raise

    def snapshot(self) -> Dict[str, int]:
        return {
            "initial_quota": self.initial_quota,
            "remaining_quota": self.remaining_quota,
            "min_reserve": self.min_reserve,
            "completed": len(self.completed_tasks),
            "rejected": len(self.rejected_tasks),
            "rolled_back": len(self.rolled_back_tasks),
        }
