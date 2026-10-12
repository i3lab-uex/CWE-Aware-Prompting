import queue
from threading import Lock

# Global task queue and a set to keep track of added task IDs.
task_queue: queue.Queue = queue.Queue()
_added_task_ids: set[str] = set()
# Lock to protect the _added_task_ids set from concurrent access.
_id_lock: Lock = Lock()


def add_task_to_queue(task_id: str, task_data: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task. Must be non-empty.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False otherwise (e.g., invalid input or duplicate ID).

    Notes
    -----
    * The function is thread‑safe. It uses a lock only when accessing the
      global `_added_task_ids` set to avoid race conditions.
    * It validates input types and ensures `task_id` is unique before
      enqueuing. If the ID already exists, the function returns False.
    * No exceptions are raised; all error conditions result in a
      `False` return value.
    """
    # Basic input validation
    if not isinstance(task_id, str) or not task_id:
        return False

    if not isinstance(task_data, dict):
        return False

    # Ensure uniqueness of task_id
    with _id_lock:
        if task_id in _added_task_ids:
            return False  # duplicate ID
        # Mark as added to prevent concurrent duplicates
        _added_task_ids.add(task_id)

    try:
        # The queue itself is thread‑safe; we simply put the task.
        task_queue.put((task_id, task_data))
    except Exception:
        # If the put fails (unlikely), remove the ID from the set
        with _id_lock:
            _added_task_ids.discard(task_id)
        return False

    return True