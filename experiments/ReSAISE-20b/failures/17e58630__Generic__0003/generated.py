import queue
import threading
from typing import Dict

# Global task queue and its lock for thread‑safety
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue()
_task_lock = threading.Lock()


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        Unique identifier for the task.
    details : dict
        Task parameters and associated data.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    try:
        # Ensure atomicity of the enqueue operation
        with _task_lock:
            task_queue.put((identifier, details))
        return True
    except Exception:
        # In a real system you might log the exception here.
        return False