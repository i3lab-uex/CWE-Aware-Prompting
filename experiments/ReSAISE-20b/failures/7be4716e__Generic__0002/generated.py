import queue

# Global task queue used by the system.
task_queue = queue.Queue()


def enqueue_task(unique_id: str, task_info: dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully added, False otherwise.
    """
    try:
        # Basic validation to avoid malformed entries
        if not isinstance(unique_id, str) or not unique_id:
            return False
        if not isinstance(task_info, dict):
            return False

        # Wrap the task data in a tuple for consistent handling
        task_payload = (unique_id, task_info)

        # Put the payload into the queue; this is thread-safe
        task_queue.put(task_payload, block=False)
        return True
    except queue.Full:
        # Queue capacity reached; treat as failure
        return False
    except Exception:
        # Catch-all for any unforeseen errors; do not propagate
        return False