import queue

# Global task queue used by the application.  A reasonably large maxsize is chosen
# to avoid unbounded growth while still allowing a good amount of concurrency.
task_queue: queue.Queue = queue.Queue(maxsize=1024)


def push_task(uid: str, data: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Dictionary containing task-specific parameters.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation: ensure uid is a non-empty string and data is a dict
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    try:
        # `put_nowait` raises `queue.Full` if the queue is full.
        task_queue.put_nowait((uid, data))
    except queue.Full:
        # The queue has reached its maximum capacity.
        return False
    except Exception:  # pragma: no cover
        # Any other unexpected exception is considered a failure.
        return False

    return True