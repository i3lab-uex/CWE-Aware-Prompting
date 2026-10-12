# queue_task.py

import threading
from queue import Queue, Full, Empty
from typing import Dict, Any

# Global task queue (thread‑safe).  It is lazily initialized on first use.
_task_queue_lock = threading.Lock()
_task_queue: Queue[Dict[str, Any]] | None = None


def _get_task_queue() -> Queue[Dict[str, Any]]:
    """Return the global task queue, creating it if necessary."""
    global _task_queue
    with _task_queue_lock:
        if _task_queue is None:
            # The queue size can be tuned; None means infinite.
            _task_queue = Queue(maxsize=0)
    return _task_queue


def queue_new_task(unique_task_id: str, task_info: Dict[str, Any]) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    unique_task_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate inputs
    if not isinstance(unique_task_id, str) or not unique_task_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Assemble the task payload
    task_payload = {"id": unique_task_id, "info": task_info}

    try:
        queue = _get_task_queue()
        # Use put_nowait to avoid blocking; return False if the queue is full
        queue.put_nowait(task_payload)
    except Full:
        return False
    except Exception:
        # Catch any unforeseen exception to satisfy the "no raise" contract
        return False

    return True