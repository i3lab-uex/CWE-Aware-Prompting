import queue
import threading
from typing import Dict

# Global task queue with a hard limit to avoid unlimited resource allocation (CWE‑770).
# The maxsize is set to 10_000 tasks; adjust as appropriate for your environment.
TASK_QUEUE_MAXSIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=TASK_QUEUE_MAXSIZE)

# A lock is not strictly necessary because Queue methods are thread‑safe,
# but it makes the code clearer and allows us to guard additional checks if needed.
_lock = threading.Lock()


def push_task(uid: str, data: Dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    uid : str
        A unique identifier for the task.
    data : dict
        Parameters and details of the task.

    Returns
    -------
    bool
        True if the task was added to the queue, False otherwise.
    """
    # Basic input validation
    if not isinstance(uid, str) or not uid:
        return False

    if not isinstance(data, dict):
        return False

    # Attempt to enqueue the task without blocking.
    try:
        with _lock:
            if task_queue.full():
                # Queue is at capacity; reject the new task.
                return False
            # Store a tuple of (uid, data) for later processing.
            task_queue.put_nowait((uid, data))
        return True
    except queue.Full:
        # In the unlikely event of a race condition, handle gracefully.
        return False
    except Exception:
        # Catch all unexpected errors to avoid leaking stack traces.
        return False