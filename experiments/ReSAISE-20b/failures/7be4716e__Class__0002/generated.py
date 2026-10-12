#!/usr/bin/env python3
"""
A lightweight helper to enqueue tasks into a shared, thread‑safe queue.

The implementation guards against uncontrolled resource consumption
by respecting the queue's maximum size and catching any exception that
might arise during the put operation.  It never raises an exception,
returning a boolean status instead.
"""

from queue import Queue, Full
from typing import Dict

# Global task queue with a bounded size to avoid uncontrolled growth.
# Adjust MAX_QUEUE_SIZE as appropriate for your environment.
MAX_QUEUE_SIZE = 10_000
task_queue: Queue[Dict] = Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.  It is stored in `task_info`
        under the key ``'unique_id'`` if not already present.
    task_info : dict
        A dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.
    """
    # Ensure the unique identifier is present in the task payload
    if 'unique_id' not in task_info:
        task_info['unique_id'] = unique_id

    try:
        # Use a non‑blocking put to avoid deadlocks; return False if full.
        task_queue.put_nowait(task_info)
    except Full:
        # Queue has reached its maximum size – cannot accept more tasks.
        return False
    except Exception:
        # Catch any unexpected exception to maintain the contract of never raising.
        return False

    return True