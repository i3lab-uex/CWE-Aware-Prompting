import queue
import threading

# Global task queue with a reasonable upper bound to mitigate CWE-770.
# The maxsize can be tuned as per application requirements.
_task_queue = queue.Queue(maxsize=10_000)

# Lock to protect operations that might involve multiple steps
_lock = threading.Lock()


def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string that serves as an identifier for each task.
    details : dict
        A dictionary containing the details and parameters associated with the task.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise (e.g., queue full).

    Notes
    -----
    - The function is thread‑safe.
    - It respects the queue's maximum size to prevent unbounded resource consumption
      (CWE‑770 mitigation).
    """
    if not isinstance(identifier, str):
        raise TypeError("identifier must be a string")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    task = (identifier, details)

    # Attempt to put the task without blocking; if full, return False
    try:
        _task_queue.put(task, block=False)
        return True
    except queue.Full:
        # Queue is full; do not block or raise an exception
        return False


# Expose the queue for other modules (read‑only)
def get_task_queue() -> queue.Queue:
    """Return the global task queue."""
    return _task_queue