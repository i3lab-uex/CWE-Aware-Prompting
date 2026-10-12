import queue
from threading import Lock

# Global task queue with a bounded size to avoid uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE according to your system's capacity.
MAX_QUEUE_SIZE = 1000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# A lock to protect the check-and-put operation when using non-blocking put.
_lock = Lock()

def push_task(uid: str, data: dict) -> bool:
    """
    Add a new task identified by `uid` and containing `data` to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Parameters or details associated with the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.

    Notes
    -----
    - The function is thread‑safe.
    - It respects the queue's maximum size to prevent uncontrolled resource consumption
      (CWE‑400).
    - The task is represented as a tuple `(uid, data)` to keep the queue generic.
    """
    # Basic validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    try:
        # Use a lock to perform a quick check and put operation atomically.
        with _lock:
            if task_queue.full():
                return False
            # Non‑blocking put; should succeed because we just checked full().
            task_queue.put_nowait((uid, data))
        return True
    except queue.Full:
        # In the unlikely event that the queue became full between check and put.
        return False
    except Exception:
        # Unexpected errors are swallowed to keep the API simple.
        return False