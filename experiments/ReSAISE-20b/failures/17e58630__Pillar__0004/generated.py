import queue

# Global task queue (should be initialized elsewhere in the application)
# Example: task_queue = queue.Queue(maxsize=1000)
try:
    # Try to use the existing global variable if defined
    task_queue  # noqa: F821
except NameError:
    # If not defined, create a default unbounded queue for demonstration purposes
    task_queue = queue.Queue()


def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        A dictionary containing parameters for the task.

    Returns
    -------
    bool
        ``True`` if the task was added successfully, ``False`` otherwise.

    Notes
    -----
    - The function validates the argument types and does not raise exceptions on failure.
    - It uses a thread‑safe queue to avoid race conditions in concurrent environments.
    """
    # Basic type validation
    if not isinstance(identifier, str) or not isinstance(details, dict):
        return False

    # Build the task payload
    task = {"id": identifier, "details": details}

    try:
        # Non‑blocking put; if the queue is full, we consider it a failure
        task_queue.put_nowait(task)
    except queue.Full:
        # Queue is at capacity – cannot enqueue
        return False
    except Exception:
        # Any other unexpected error (shouldn't happen with Queue)
        return False

    return True