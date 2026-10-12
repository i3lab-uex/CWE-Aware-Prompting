import queue

# Global task queue used by the application.
# It is thread‑safe, so no additional locking is required for simple operations.
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue()

def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        A dictionary containing all parameters required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was added successfully, otherwise ``False``.

    Notes
    -----
    - The function uses the thread‑safe :class:`queue.Queue` API.
    - It performs minimal validation to avoid accidental misuse:
      * `identifier` must be a non‑empty string.
      * `details` must be a dictionary.
    - In normal operation the function will always succeed; ``False`` is returned
      only when input validation fails.
    """
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    try:
        task_queue.put_nowait((identifier, details))
    except queue.Full:  # pragma: no cover – queue is unbounded by default
        return False

    return True