#!/usr/bin/env python3
"""
Thread‑safe task queue with resource limits.
"""

import threading
from queue import Queue, Full

# Global configuration -------------------------------------------------------

MAX_QUEUE_SIZE = 10_000          # Maximum number of pending tasks
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)
# Keeps track of task IDs that are already queued to avoid duplicates
queued_task_ids: set[str] = set()
# Lock protects the set of IDs (queue operations are already thread‑safe)
id_lock = threading.Lock()


# Public API -----------------------------------------------------------------

def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
        The function will return False if the queue is full or a task with
        the same ID already exists in the queue.

    Notes
    -----
    * The function is thread‑safe.
    * It protects against uncontrolled resource consumption by enforcing a
      maximum queue size and preventing duplicate task IDs.
    """
    # Basic validation -------------------------------------------------------
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Ensure the task ID is unique ------------------------------------------------
    with id_lock:
        if task_id in queued_task_ids:
            return False

    # Attempt to enqueue --------------------------------------------------------
    try:
        task_queue.put_nowait((task_id, task_data))
    except Full:
        return False

    # Record the ID after successful enqueue -----------------------------------
    with id_lock:
        queued_task_ids.add(task_id)

    return True


# Optional helper for workers ----------------------------------------------
def pop_task_from_queue() -> tuple[str, dict] | None:
    """
    Retrieve the next task from the queue.

    Returns
    -------
    tuple[str, dict] | None
        The next task ID and data, or None if the queue is empty.
    """
    try:
        task_id, task_data = task_queue.get_nowait()
    except Exception:  # queue.Empty
        return None

    with id_lock:
        queued_task_ids.discard(task_id)

    task_queue.task_done()
    return task_id, task_data