import threading
from queue import Queue, Full

# Global task queue shared across threads.
# Adjust maxsize as needed; 0 means infinite.
task_queue = Queue(maxsize=0)

# Lock to guard any additional shared state if needed in the future.
_queue_lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Add a task identified by `uid` with its associated `data` to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Parameters and details of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    task = (uid, data)

    try:
        # Use a non-blocking put to avoid hanging the caller.
        task_queue.put_nowait(task)
    except Full:
        # Queue is full; could log or handle differently.
        return False
    except Exception:
        # Unexpected error; do not raise to caller.
        return False

    return True