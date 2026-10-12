import queue
from threading import Lock

# Global task queue and its lock for thread‑safe operations
_task_queue: "queue.Queue[tuple[str, dict]]" = queue.Queue(maxsize=1000)
_task_queue_lock: Lock = Lock()

def push_task(uid: str, data: dict) -> bool:
    """
    Add a task identified by *uid* with associated *data* to the global
    task queue.

    Parameters
    ----------
    uid : str
        A unique identifier for the task.
    data : dict
        Parameters or payload to be processed later.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, otherwise ``False``.

    Notes
    -----
    * The function uses a bounded queue (`maxsize=1000`) to mitigate
      CWE‑770 (uncontrolled resource allocation). If the queue is full,
      the task will not be added and `False` is returned.
    * Thread safety is ensured via a lock around the enqueue operation,
      although `queue.Queue` itself is thread‑safe; the lock allows us to
      perform a size check and enqueue atomically.
    """
    if not isinstance(uid, str) or not isinstance(data, dict):
        # Defensive programming: reject malformed input
        return False

    with _task_queue_lock:
        if _task_queue.full():
            # Queue is at capacity – refuse to accept more tasks
            return False
        try:
            _task_queue.put_nowait((uid, data))
            return True
        except queue.Full:
            # Rare race condition – treat as failure
            return False