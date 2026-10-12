# -*- coding: utf-8 -*-
"""
Task queue implementation with bounded capacity to mitigate CWE‑770.

The global `task_queue` is a thread‑safe FIFO queue that holds tasks
represented as `(identifier, content)` tuples. The maximum size is set to
`MAX_QUEUE_SIZE`; attempts to enqueue when the queue is full return `False`
instead of blocking or raising an exception.
"""

from __future__ import annotations

import queue
from typing import Dict, Tuple

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Maximum number of tasks that may be queued simultaneously.
MAX_QUEUE_SIZE: int = 1_000

# --------------------------------------------------------------------------- #
# Global queue
# --------------------------------------------------------------------------- #

#: The shared task queue.  `queue.Queue` is inherently thread‑safe.
task_queue: queue.Queue[Tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_content : dict
        A dictionary containing the task's parameters and data.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, ``False`` if the
        queue is full and the task could not be added.

    Notes
    -----
    * The function never raises an exception; it simply returns ``False``
      when the queue is at capacity.
    * Because :class:`queue.Queue` enforces a maximum size, this
      implementation protects against unbounded memory consumption,
      addressing CWE‑770.
    """
    # Validate input types for defensive programming (optional but useful)
    if not isinstance(task_identifier, str):
        raise TypeError("task_identifier must be a string")
    if not isinstance(task_content, dict):
        raise TypeError("task_content must be a dictionary")

    # Attempt to enqueue without blocking; if full, return False.
    try:
        task_queue.put_nowait((task_identifier, task_content))
        return True
    except queue.Full:
        # Queue has reached its maximum capacity.
        return False

# --------------------------------------------------------------------------- #
# Example usage (for local testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Basic demonstration of enqueuing tasks
    for i in range(5):
        success = insert_task_to_queue(f"task_{i}", {"param": i})
        print(f"Enqueue task_{i}: {'Success' if success else 'Failed'}")