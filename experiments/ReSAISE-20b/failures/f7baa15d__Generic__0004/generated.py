import queue
import threading
from typing import Dict

# Global task queue (thread‑safe)
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue()

# A set to keep track of existing task IDs for quick duplicate checks
_task_ids_lock = threading.Lock()
_existing_task_ids: set[str] = set()


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        A dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    # Basic validation
    if not isinstance(task_id, str) or not task_id:
        return False
    if not isinstance(task_data, dict):
        return False

    # Ensure the task ID is unique across all pending tasks
    with _task_ids_lock:
        if task_id in _existing_task_ids:
            return False
        # Mark as pending
        _existing_task_ids.add(task_id)

    try:
        task_queue.put_nowait((task_id, task_data))
    except queue.Full:  # pragma: no cover
        # If the queue is full, remove the ID marker to allow future retries
        with _task_ids_lock:
            _existing_task_ids.discard(task_id)
        return False

    return True