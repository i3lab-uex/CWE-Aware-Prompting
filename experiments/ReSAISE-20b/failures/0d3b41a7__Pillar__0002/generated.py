import threading
from queue import Queue
from typing import Dict

# Global task queue and a set to track unique IDs.
_task_queue: Queue[Dict] = Queue()
_active_ids: set[str] = set()

# Lock to guard access to _active_ids and enqueue operation.
_queue_lock = threading.RLock()


def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters.

    Returns
    -------
    bool
        True if the task was enqueued; False if a duplicate ID or enqueue failure.
    """
    # Basic validation
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    with _queue_lock:
        # Check for duplicate ID
        if unique_task_id in _active_ids:
            return False

        # Prepare the task payload
        task_payload = {"id": unique_task_id, "info": task_info}

        try:
            _task_queue.put_nowait(task_payload)
            _active_ids.add(unique_task_id)
        except Exception:
            # If the queue is full or another error occurs, do not add the ID.
            return False

    return True