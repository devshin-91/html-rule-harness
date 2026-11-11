"""Runtime Task Queue with retry guard and token rate telemetry (Sub-task T3 seed)."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class QueuedTask:
    task_id: str
    payload: str
    max_retries: int = 2
    attempts: int = 0
    status: str = "pending"


class TaskQueue:
    """Manages queued agent tasks, retry limits, and token throughput metrics."""

    # BUG 1: Mutable default argument `initial_tags=[]` leaks state across TaskQueue instances
    def __init__(self, initial_tags: Optional[List[str]] = None) -> None:
        self.tags: List[str] = list(initial_tags) if initial_tags is not None else []
        self._tasks: Dict[str, QueuedTask] = {}

    def add_tag(self, tag: str) -> None:
        """Attach a metadata tag to this queue instance."""
        if tag not in self.tags:
            self.tags.append(tag)

    def enqueue(self, task_id: str, payload: str, max_retries: int = 2) -> QueuedTask:
        """Add a new task to the queue."""
        if not task_id:
            raise ValueError("task_id must be non-empty")
        task = QueuedTask(task_id=task_id, payload=payload, max_retries=max_retries)
        self._tasks[task_id] = task
        return task

    def record_failure(self, task_id: str) -> str:
        """Increment failure attempts and transition status to 'failed' once retries are exhausted.

        A task with max_retries=2 should allow 2 retries (i.e. fail permanently when attempts > max_retries,
        or on the (max_retries + 1)-th failure).
        """
        if task_id not in self._tasks:
            raise KeyError(f"Unknown task_id: {task_id}")
        task = self._tasks[task_id]
        task.attempts += 1
        # BUG 2: Off-by-one comparison (`>=` instead of `>`) marks the task permanently failed
        # on the 2nd failure even when max_retries=2 allows 2 retries (3 total attempts).
        if task.attempts > task.max_retries:
            task.status = "failed"
        else:
            task.status = "retrying"
        return task.status

    @staticmethod
    def compute_tokens_per_second(total_tokens: int, elapsed_seconds: float) -> float:
        """Compute token throughput (tokens/sec), returning 0.0 when elapsed_seconds <= 0."""
        if total_tokens < 0:
            raise ValueError("total_tokens cannot be negative")
        # BUG 3: ZeroDivisionError (and negative rate) when elapsed_seconds <= 0
        if elapsed_seconds <= 0:
            return 0.0
        return round(total_tokens / elapsed_seconds, 2)
