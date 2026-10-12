# enqueue_task.py

"""
A thread‑safe helper to add a task into the global `task_queue`.
It ensures that resources are properly controlled and that no
exceptions leak out to the caller.  The function returns a boolean
indicating whether the task was successfully enqueued.
"""

import queue
from typing import Dict

# Global queue used by the system (must be initialised elsewhere)
task_queue: queue.Queue | None = None


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Insert a new task into the shared `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    - The function never raises; it catches any exception that might occur
      during the enqueue operation and returns ``False``.
    - If `task_queue` is not initialised, the function will also return ``False``.
    """
    global task_queue

    if task_queue is None:
        # Queue not initialised – cannot proceed
        return False

    # Build the task payload; include unique_id to avoid accidental duplicates
    payload = {"unique_id": unique_id, "task_info": task_info}

    try:
        # Non‑blocking put to avoid deadlock if the queue is full
        task_queue.put_nowait(payload)
    except (queue.Full, Exception):
        # Either the queue is full or an unexpected error occurred
        return False

    return True