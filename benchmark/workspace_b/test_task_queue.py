"""Unit tests for TaskQueue (Sub-task T3 verifier)."""

import unittest
from task_queue import TaskQueue


class TestTaskQueue(unittest.TestCase):
    def test_instance_tag_isolation(self) -> None:
        q1 = TaskQueue()
        q2 = TaskQueue()
        q1.add_tag("batch-a")
        self.assertEqual(q1.tags, ["batch-a"])
        self.assertEqual(q2.tags, [])

    def test_retry_threshold_exact(self) -> None:
        q = TaskQueue()
        q.enqueue("t-1", "run analysis", max_retries=2)
        # 1st failure -> retry #1 allowed
        self.assertEqual(q.record_failure("t-1"), "retrying")
        # 2nd failure -> retry #2 allowed
        self.assertEqual(q.record_failure("t-1"), "retrying")
        # 3rd failure -> retries exhausted (attempts=3 > max_retries=2)
        self.assertEqual(q.record_failure("t-1"), "failed")

    def test_tokens_per_second_zero_elapsed(self) -> None:
        self.assertEqual(TaskQueue.compute_tokens_per_second(1200, 4.0), 300.0)
        self.assertEqual(TaskQueue.compute_tokens_per_second(500, 0.0), 0.0)
        self.assertEqual(TaskQueue.compute_tokens_per_second(500, -1.5), 0.0)

    def test_boundary_regression_conditions(self) -> None:
        caller_tags = ["init"]
        q_none = TaskQueue(None)
        q_list = TaskQueue(caller_tags)
        caller_tags.append("mutated")
        self.assertEqual(q_none.tags, [])
        self.assertEqual(q_list.tags, ["init"])
        q_none.enqueue("zero-retry", "payload", max_retries=0)
        self.assertEqual(q_none.record_failure("zero-retry"), "failed")
        self.assertEqual(TaskQueue.compute_tokens_per_second(0, 1.0), 0.0)


if __name__ == "__main__":
    unittest.main()
