import queue
from typing import Dict

# Global task queue – unbounded by default (maxsize=0)
task_queue: queue.Queue = queue.Queue(maxsize=0)


def push_task(uid: str, data: Dict) -> bool:
    """
    Safely add a task to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Task payload.

    Returns
    -------
    bool
        True if the task was queued, False otherwise.
    """
    # Basic type validation – prevents accidental misuse
    if not isinstance(uid, str) or not isinstance(data, dict):
        return False

    try:
        # queue.Queue is thread‑safe; use put_nowait to avoid blocking
        task_queue.put_nowait((uid, data))
    except queue.Full:
        # Queue is full (unlikely with maxsize=0 but handled for safety)
        return False
    except Exception:
        # Any other unexpected error should not propagate
        return False

    return True