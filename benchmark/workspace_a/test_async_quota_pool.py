"""Concurrency stress tests for AsyncQuotaPool (Sub-task T4 verifier)."""

import asyncio
import unittest
from async_quota_pool import AsyncQuotaPool


class TestAsyncQuotaPool(unittest.TestCase):
    def test_concurrent_50_workers_never_overspend(self) -> None:
        async def run_stress_iteration() -> None:
            # 100 initial, 10 min_reserve -> exactly 90 usable units -> at cost=3, max 30 tasks can succeed
            pool = AsyncQuotaPool(initial_quota=100, min_reserve=10)

            async def worker(i: int) -> bool:
                return await pool.allocate_and_run(f"worker-{i}", cost=3, simulate_fail=False)

            results = await asyncio.gather(*(worker(i) for i in range(50)))
            succeeded = sum(1 for r in results if r)
            rejected = sum(1 for r in results if not r)

            self.assertEqual(succeeded, 30, f"Expected exactly 30 successes, got {succeeded}")
            self.assertEqual(rejected, 20, f"Expected exactly 20 rejections, got {rejected}")
            self.assertEqual(pool.remaining_quota, 10, f"Quota dropped to {pool.remaining_quota} (< 10)")

        async def run_all() -> None:
            for _ in range(5):
                await run_stress_iteration()

        asyncio.run(run_all())

    def test_rollback_on_worker_exception_and_reallocate(self) -> None:
        async def scenario() -> None:
            pool = AsyncQuotaPool(initial_quota=20, min_reserve=5)
            # Usable = 15. Run 3 failing workers (cost=5 each) concurrently: all must rollback!
            tasks = [
                pool.allocate_and_run(f"fail-{i}", cost=5, simulate_fail=True)
                for i in range(3)
            ]
            outcomes = await asyncio.gather(*tasks, return_exceptions=True)
            self.assertEqual(len(outcomes), 3)
            for out in outcomes:
                self.assertIsInstance(out, RuntimeError)

            # Because all 3 rolled back, remaining_quota must be restored to 20
            self.assertEqual(pool.remaining_quota, 20)
            self.assertEqual(len(pool.rolled_back_tasks), 3)

            # Subsequent valid worker of cost=15 must succeed
            ok = await pool.allocate_and_run("valid-after-rollback", cost=15, simulate_fail=False)
            self.assertTrue(ok)
            self.assertEqual(pool.remaining_quota, 5)

        asyncio.run(scenario())


if __name__ == "__main__":
    unittest.main()
