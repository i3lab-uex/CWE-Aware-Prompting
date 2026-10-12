# queue_new_task.py

"""
A thread‑safe task enqueuing helper for a multi‑threaded system.

The module keeps a global FIFO queue (`task_queue`) with an optional maximum
size to mitigate uncontrolled resource consumption (CWE‑400).  Each task is
identified by a unique string; duplicate IDs are rejected.  The function
`queue_new_task` returns ``True`` when the task is enqueued, otherwise
``False``.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import threading
from queue import Queue, Full
from typing import Dict

# ------------------------------
# Configuration
# ------------------------------

MAX_QUEUE_SIZE: int = 10_000  # maximum number of pending tasks

# ------------------------------
# Global state
# ------------------------------

# The task queue itself – FIFO, thread‑safe.
task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Set of IDs already in the queue or processed.  Protected by `id_lock`.
queued_task_ids: set[str] = set()
id_lock = threading.Lock()


# ------------------------------
# Public API
# ------------------------------

def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.  Duplicate IDs are rejected.
    task_info : dict
        Dictionary containing the task's specifics and parameters.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, ``False`` otherwise.

    Notes
    -----
    * The function is thread‑safe.
    * If the queue has reached `MAX_QUEUE_SIZE` or if the ID already exists,
      the task is not added and ``False`` is returned.
    """
    # Quick validation of inputs
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False

    if not isinstance(task_info, dict):
        return False

    # Acquire lock to check and update the ID set atomically
    with id_lock:
        if unique_task_id in queued_task_ids:
            # Duplicate ID – reject
            return False

        # Reserve the ID before attempting to enqueue
        queued_task_ids.add(unique_task_id)

    try:
        # Try to put the task into the queue without blocking
        task_queue.put_nowait((unique_task_id, task_info))
    except Full:
        # Queue is full – remove the reserved ID and fail
        with id_lock:
            queued_task_ids.discard(unique_task_id)
        return False

    # Task enqueued successfully
    return True


# ------------------------------
# Optional helper: dequeue and process
# ------------------------------

def get_next_task() -> tuple[str, Dict] | None:
    """
    Retrieve the next task from the queue.  Returns ``None`` if no tasks are
    available.

    This function removes the task ID from `queued_task_ids` so that a new
    task with the same ID can be queued later.
    """
    try:
        unique_task_id, task_info = task_queue.get_nowait()
    except Exception:  # Queue.Empty
        return None

    with id_lock:
        queued_task_ids.discard(unique_task_id)

    # Mark the task as processed in the queue
    task_queue.task_done()
    return unique_task_id, task_info