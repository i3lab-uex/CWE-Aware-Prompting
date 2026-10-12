#!/usr/bin/env python3
"""
Utility to safely push tasks into a global queue.

The implementation protects against uncontrolled resource consumption
by respecting the queue's maximum size.  If the queue is full, the task
is not added and the function returns False.

Author: OpenAI ChatGPT
"""

from queue import Queue, Full
from typing import Dict

# Global task queue.  In a real system this would be created elsewhere
# and imported, but for completeness we instantiate it here with a
# reasonable maximum size.
task_queue: Queue = Queue(maxsize=1000)  # adjust as needed


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Safely push a task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        True if the task was added to the queue, False otherwise.
    """
    # Basic validation
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Attempt to add the task without blocking.
    try:
        task_queue.put_nowait((task_uid, task_info))
    except Full:
        # Queue is full – cannot accept new tasks at this time.
        return False
    except Exception:
        # Catch-all for unexpected errors; do not raise to caller.
        return False

    return True