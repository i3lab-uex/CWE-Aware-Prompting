import queue

# Global task queue – assumed to be defined elsewhere in the application.
# For illustration purposes, we create a default instance here.
task_queue: queue.Queue = queue.Queue(maxsize=0)  # unbounded


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global `task_queue`.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        The payload or configuration associated with the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_reference, str) or not task_reference:
        return False

    if not isinstance(parameters, dict):
        return False

    # Construct the task entry
    task_entry = (task_reference, parameters)

    try:
        # Use put_nowait to avoid blocking; if the queue is full, return False
        task_queue.put_nowait(task_entry)
    except queue.Full:
        # The queue is at capacity; task cannot be added
        return False

    return True