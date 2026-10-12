import queue

# Global task queue used by the system.  It must be initialized elsewhere in the
# application before any calls to `enqueue_task` are made.
task_queue: queue.Queue = None  # type: ignore


def enqueue_task(unique_id: str, task_info: dict) -> bool:
    """
    Safely insert a new task into the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task. Must be a non-empty string.
    task_info : dict
        A dictionary containing all information required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    * The function performs basic type checking to guard against accidental misuse.
    * It attempts a non‑blocking put; if the queue is full it returns ``False``.
    * Any unexpected exception is caught and results in a ``False`` return value,
      preventing the caller from crashing due to queue errors.
    """
    # Validate arguments
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Ensure the global queue is available
    if task_queue is None:
        return False

    try:
        # Attempt to enqueue without blocking; this prevents the process from
        # hanging if the queue is full.
        task_queue.put((unique_id, task_info), block=False)
    except queue.Full:
        # Queue capacity reached – indicate failure
        return False
    except Exception:
        # Any other exception (e.g., serialization errors) is treated as a failure
        return False

    return True