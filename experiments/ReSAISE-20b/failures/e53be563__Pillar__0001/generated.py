import threading
from queue import Queue, Full

# Global task queue (unbounded).  The actual size can be configured if needed.
task_queue = Queue()

# A lock to guard against potential race conditions when checking for duplicates
# (if such logic is added in the future).  The Queue itself is thread‑safe.
_task_lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Add a task identified by *uid* and associated with *data* to the global
    :data:`task_queue`.

    Parameters
    ----------
    uid: str
        Unique identifier for the task.  The function does not enforce uniqueness,
        but callers may do so if required.
    data: dict
        Arbitrary task payload.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    - The function uses :meth:`queue.Queue.put_nowait` to avoid blocking.  If the
      queue is full (in a bounded configuration) it returns ``False``.
    - The implementation guards against accidental duplicate enqueues in the
      future by wrapping the operation with a lock, but currently it simply
      enqueues without checking for duplicates.
    """
    try:
        # The Queue is thread‑safe; the lock is defensive for future extensions.
        with _task_lock:
            task_queue.put_nowait((uid, data))
        return True
    except Full:
        # Queue is full in a bounded configuration.
        return False
    except Exception:
        # Catch any unforeseen exceptions to ensure the function never raises.
        return False