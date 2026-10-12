#!/usr/bin/env python3
"""
Utility for adding a task to the global processing queue.

The function checks input types, guards against exceeding the queue's
maximum size (to avoid uncontrolled resource consumption), and returns
a boolean indicating success or failure.  No exceptions are propagated
to callers.
"""

from queue import Queue, Full
from typing import Dict

# Global task queue – assumed to be created elsewhere in the system.
# For demonstration, we create a default instance if not already defined.
try:
    task_queue  # type: ignore
except NameError:
    task_queue = Queue(maxsize=1000)  # Adjust maxsize as needed


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully,
        ``False`` otherwise (e.g., queue full, invalid inputs).
    """
    # Validate input types
    if not isinstance(task_uid, str) or not isinstance(task_info, dict):
        return False

    # Basic sanity checks on task content
    if not task_uid.strip() or not task_info:
        return False

    # Try to enqueue without blocking; catch Full exception if queue limit reached
    try:
        task_queue.put((task_uid, task_info), block=False)
    except Full:
        # Queue is full – reject the new task to prevent uncontrolled growth
        return False
    except Exception:
        # Any other unforeseen error – log if needed, but do not propagate
        return False

    return True