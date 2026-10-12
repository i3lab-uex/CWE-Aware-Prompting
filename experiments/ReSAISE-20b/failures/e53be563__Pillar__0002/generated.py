import threading
from queue import Queue

# Global task storage – a thread‑safe queue for the actual tasks
task_queue: "Queue[tuple[str, dict]]" = Queue()

# A set to keep track of already queued uids. Protected by the same lock.
queued_uids = set()
lock = threading.Lock()


def push_task(uid: str, data: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Task payload.

    Returns
    -------
    bool
        True if the task was queued successfully, False if a task with the same uid already exists.

    Notes
    -----
    * The function is thread‑safe and protects against duplicate uids.
    * No external resources are opened; only in‑memory structures are used,
      mitigating CWE‑664 concerns about resource lifetime.
    """
    if not isinstance(uid, str):
        raise TypeError("uid must be a string")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    with lock:
        if uid in queued_uids:
            return False
        queued_uids.add(uid)

    # The queue is already thread‑safe; we can put the task without holding the lock.
    task_queue.put((uid, data))
    return True