# ──────────────────────────────────────────────────────────────
#  enqueue_task – thread‑safe addition to a bounded global queue
# ──────────────────────────────────────────────────────────────

import threading
from queue import Queue, Full

# ------------------------------------------------------------------
# Global task queue – bounded to mitigate CWE‑770 (resource exhaustion).
# Adjust `MAX_QUEUE_SIZE` as appropriate for your environment.
# ------------------------------------------------------------------
MAX_QUEUE_SIZE = 10_000   # Example limit; tune per deployment
_task_queue_lock = threading.Lock()
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Safely add a task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        Unique string that identifies the task.
    details : dict
        Dictionary containing parameters for the task.

    Returns
    -------
    bool
        ``True`` if the task was queued successfully, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    # Attempt non‑blocking enqueue to avoid resource exhaustion
    try:
        with _task_queue_lock:          # Ensure atomicity in multi‑threaded contexts
            task_queue.put_nowait((identifier, details))
        return True
    except Full:
        # Queue has reached its maximum capacity; task is rejected.
        return False