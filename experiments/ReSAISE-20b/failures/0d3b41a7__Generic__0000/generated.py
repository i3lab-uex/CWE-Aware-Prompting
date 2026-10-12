# queue_new_task.py

"""
Task queuing utility for a multi‑threaded system.

The module defines a global `task_queue` and a helper function
`queue_new_task` that safely enqueues tasks.  Each task is identified by a
unique string `task_id`.  The function returns ``True`` when the task is
successfully added and ``False`` if a duplicate ID is detected or an
exception occurs during enqueuing.

Author: ChatGPT
"""

from __future__ import annotations

import queue
import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global task queue and supporting data structures
# --------------------------------------------------------------------------- #

#: A thread‑safe FIFO queue that stores tasks as ``(task_id, task_info)`` tuples.
task_queue: "queue.Queue[tuple[str, dict]]" = queue.Queue()

#: A set that keeps track of all task IDs currently in the queue.  Protect it
#: with a lock to avoid race conditions.
_task_id_set: set[str] = set()
_task_id_lock = threading.Lock()

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def queue_new_task(unique_task_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Append a new task to the global :data:`task_queue`.

    Parameters
    ----------
    unique_task_id:
        A unique string identifier for the task.  If a task with the same ID
        already exists in the queue, the function returns ``False``.
    task_info:
        A dictionary containing the task's parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    - The function is thread‑safe: it acquires :data:`_task_id_lock` before
      checking and updating the ID set.
    - No exceptions are raised; errors during queue operations result in
      a ``False`` return value.
    """
    # Validate input types (optional but helps catch misuse early)
    if not isinstance(unique_task_id, str):
        raise TypeError("unique_task_id must be a string")
    if not isinstance(task_info, dict):
        raise TypeError("task_info must be a dictionary")

    # Acquire lock to check for duplicate IDs safely
    with _task_id_lock:
        if unique_task_id in _task_id_set:
            # Duplicate ID detected; do not enqueue
            return False

        # Reserve the ID before actually enqueuing to avoid race conditions
        _task_id_set.add(unique_task_id)

    try:
        # Enqueue the task.  The operation is atomic and thread‑safe.
        task_queue.put((unique_task_id, task_info), block=False)
    except queue.Full:
        # The queue is full (unlikely with default unbounded Queue).
        # Release the ID reservation and signal failure.
        with _task_id_lock:
            _task_id_set.discard(unique_task_id)
        return False
    except Exception:
        # Any other unexpected exception: clean up and signal failure.
        with _task_id_lock:
            _task_id_set.discard(unique_task_id)
        return False

    # Success
    return True


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove if running as a module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Enqueue some sample tasks
    assert queue_new_task("task1", {"param": 42})
    assert not queue_new_task("task1", {"param": "duplicate"})  # duplicate ID

    # Dequeue and process tasks
    while not task_queue.empty():
        t_id, t_info = task_queue.get()
        print(f"Processing {t_id}: {t_info}")