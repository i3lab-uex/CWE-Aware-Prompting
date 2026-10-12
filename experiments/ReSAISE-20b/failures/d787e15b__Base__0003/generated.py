# -*- coding: utf-8 -*-

"""
Utility for registering new tasks into a global task queue.

The implementation ensures that the queue does not grow unboundedly,
preventing CWE-770: Allocation of Resources Without Limits or Throttling.
"""

from __future__ import annotations

import queue
import threading
from typing import Dict, Optional

# Global task queue – set a reasonable maximum size to avoid resource exhaustion.
# Adjust `MAX_QUEUE_SIZE` as needed for the application's capacity.
_MAX_QUEUE_SIZE = 10_000
_task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=_MAX_QUEUE_SIZE)

# Optional lock for additional atomicity if needed beyond the queue's internal
# synchronization (e.g., when accessing auxiliary data structures).
_queue_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        Parameters associated with the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.

    Notes
    -----
    - The function is thread‑safe.
    - If the queue is full, the task is rejected to prevent uncontrolled memory growth.
    """
    if not isinstance(task_reference, str):
        raise TypeError("task_reference must be a string")
    if not isinstance(parameters, dict):
        raise TypeError("parameters must be a dictionary")

    # Attempt to enqueue without blocking; return False if the queue is full.
    try:
        with _queue_lock:  # optional, for any extra critical sections
            _task_queue.put_nowait((task_reference, parameters))
        return True
    except queue.Full:
        # Queue has reached its maximum size – reject the new task.
        return False


# Expose the queue for consumers; in a real application you might provide
# accessor functions instead of exposing the object directly.
def get_task_queue() -> queue.Queue[tuple[str, dict]]:
    """Return the global task queue."""
    return _task_queue