# -*- coding: utf-8 -*-
"""
Utility to push a task into the global task queue.
"""

import threading
from queue import Queue, Full

# Global task queue.  It should be initialized once by the application.
# If not already defined, create a default queue with reasonable limits.
try:
    task_queue  # type: ignore
except NameError:
    # Default to a FIFO queue with a maximum size of 10,000 tasks.
    task_queue = Queue(maxsize=10_000)

# Lock to serialize access when creating the queue or performing other one‑time
# initialisation tasks.  The queue itself is thread‑safe, but this lock guards
# the global variable.
_queue_lock = threading.Lock()


def push_task_to_queue(task_uid: str, task_info: dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    task_uid : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was queued successfully, otherwise ``False``.

    Notes
    -----
    - The function is intentionally exception‑free; any error results in a
      ``False`` return value.
    - If the queue is full, the task will not be added and ``False`` is
      returned.
    """
    # Basic type validation to avoid accidental misuse.
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Prepare the payload.  We keep the uid separate to avoid accidental
    # mutation of the original dict.
    payload = {"uid": task_uid, "info": task_info}

    try:
        # ``put_nowait`` raises ``Full`` if the queue has reached its maxsize.
        task_queue.put_nowait(payload)
    except Full:
        # Queue is full – caller can decide to retry later.
        return False
    except Exception:
        # Catch any unexpected exception and report failure.
        return False

    return True