import threading
from queue import Queue, Full

# Global task queue – unbounded by default.
task_queue: Queue = Queue()

# Lock to guard any future shared structures (currently not needed for Queue but kept for extensibility).
_queue_lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Add a task to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(uid, str):
        return False
    if not isinstance(data, dict):
        return False

    # Construct the task payload.  We keep a shallow copy to avoid accidental mutation
    # of the caller's dictionary after it has been queued.
    task_payload = {"uid": uid, "data": data.copy()}

    try:
        # Queue operations are thread‑safe, but we still guard the put operation
        # with a lock in case future extensions require additional shared state.
        with _queue_lock:
            task_queue.put_nowait(task_payload)
    except Full:  # pragma: no cover – the queue is unbounded, so this should not happen.
        return False
    except Exception:  # pragma: no cover – any unforeseen error should not crash the caller.
        return False

    return True