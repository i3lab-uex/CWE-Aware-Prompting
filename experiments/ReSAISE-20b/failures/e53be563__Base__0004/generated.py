import queue

# Assume a global task queue has been created elsewhere in the application.
# Example:
#   task_queue = queue.Queue(maxsize=1000)

def push_task(uid: str, data: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Task payload containing parameters and details.

    Returns
    -------
    bool
        True if the task was queued successfully, False otherwise.
    """
    # Validate inputs
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Compose the task entry; a tuple is used to keep ordering simple.
    task = (uid, data)

    try:
        # Attempt a non‑blocking put. If the queue is full we catch
        # queue.Full and return False to avoid unbounded growth.
        task_queue.put_nowait(task)
    except AttributeError:
        # The global queue was not defined.
        return False
    except queue.Full:
        return False

    return True