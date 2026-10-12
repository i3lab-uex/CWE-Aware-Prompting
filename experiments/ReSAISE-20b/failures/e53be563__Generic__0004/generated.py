import threading
from queue import Queue, Full

# Global task queue (FIFO). Adjust maxsize as needed; None for unlimited.
task_queue = Queue(maxsize=0)

# Lock to guard access if we need atomic operations beyond queue's own.
_queue_lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Push a new task into the global `task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Dictionary containing task parameters and details.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic validation: ensure uid is a non-empty string and data is a dict
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    task = {"uid": uid, "data": data}

    try:
        # Queue's put_nowait is thread‑safe; we still lock to protect
        # any composite operations if added later.
        with _queue_lock:
            task_queue.put_nowait(task)
    except Full:
        # Queue capacity exceeded (unlikely if maxsize is 0/unlimited)
        return False
    except Exception:
        # Catch all unexpected errors to avoid propagating.
        return False

    return True