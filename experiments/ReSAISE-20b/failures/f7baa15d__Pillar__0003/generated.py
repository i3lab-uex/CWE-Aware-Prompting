import threading
from queue import Queue
from typing import Dict

# Global task queue and set of active task IDs.
task_queue: Queue = Queue()
_active_task_ids: set[str] = set()

# Lock to protect access to _active_task_ids and task_queue
_lock = threading.RLock()


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Adds a new task to the global `task_queue`.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        A dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False otherwise (e.g., duplicate task_id or internal error).

    Notes
    -----
    - The function is thread‑safe and protects against duplicate task IDs.
    - It never raises an exception; errors are handled internally and a False
      value is returned instead.
    """
    if not isinstance(task_id, str) or not isinstance(task_data, dict):
        # Invalid input types; do not enqueue
        return False

    with _lock:
        if task_id in _active_task_ids:
            # Duplicate task; do not enqueue
            return False

        try:
            # Enqueue the task as a tuple (id, data)
            task_queue.put_nowait((task_id, task_data))
        except Exception:
            # If queue operation fails (unlikely with Queue), do not add id
            return False

        # Mark the task ID as active
        _active_task_ids.add(task_id)

    return True


# Optional: a helper to remove completed tasks from the active set.
def mark_task_completed(task_id: str) -> None:
    """
    Marks a task as completed, freeing its ID for reuse.

    Parameters
    ----------
    task_id : str
        The identifier of the completed task.
    """
    with _lock:
        _active_task_ids.discard(task_id)