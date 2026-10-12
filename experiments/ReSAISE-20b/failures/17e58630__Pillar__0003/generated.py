# -*- coding: utf-8 -*-

"""
A thread‑safe task enqueue module.

This module defines a global `task_queue` and a helper function
`enqueue_task` that safely adds tasks to the queue.  The function
validates its arguments, prevents duplicate task identifiers and
ensures that the queue is never over‑filled by using a bounded size.
"""

import threading
from queue import Queue, Full

# ----------------------------------------------------------------------
# Global data structures
# ----------------------------------------------------------------------
# The maximum number of tasks that can be queued at any one time.
MAX_QUEUE_SIZE = 1000

# A thread‑safe queue that holds task tuples: (identifier, details).
task_queue = Queue(maxsize=MAX_QUEUE_SIZE)

# A set that tracks identifiers already present in the queue.
_active_ids = set()
_lock = threading.Lock()          # protects _active_ids


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        A dictionary containing task parameters.

    Returns
    -------
    bool
        ``True`` if the task was enqueued, ``False`` otherwise.
    """
    # Basic type validation
    if not isinstance(identifier, str) or not isinstance(details, dict):
        return False

    # Avoid duplicate identifiers
    with _lock:
        if identifier in _active_ids:
            return False

        # Reserve the identifier before attempting to enqueue
        _active_ids.add(identifier)

    try:
        # The queue is bounded; if full, we block briefly instead of
        # raising an exception.  This prevents resource exhaustion.
        task_queue.put((identifier, details), timeout=1)
    except Full:
        # Queue was full; release the identifier reservation
        with _lock:
            _active_ids.discard(identifier)
        return False
    except Exception:
        # Unexpected error; clean up and fail silently
        with _lock:
            _active_ids.discard(identifier)
        return False

    # Successful enqueue
    return True


# ----------------------------------------------------------------------
# Optional helper for workers to dequeue tasks safely
# ----------------------------------------------------------------------
def _worker_fetch_task(timeout: float = 1.0):
    """
    Internal helper to fetch a task from the queue and release its
    identifier when processed.  Workers should call this function.
    """
    try:
        identifier, details = task_queue.get(timeout=timeout)
    except Exception:
        return None, None

    # After the worker finishes processing, it must call `task_queue.task_done()`
    # and remove the identifier from _active_ids.
    return identifier, details