import queue

# The global task queue should be instantiated elsewhere in the application.
# Here we provide a default placeholder to allow this module to run independently
# for testing purposes. In production, replace `task_queue` with the actual
# shared Queue instance.
try:
    task_queue  # noqa: F821 - check if already defined
except NameError:
    task_queue = queue.Queue(maxsize=1000)  # default size; adjust as needed


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
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation to guard against malformed inputs
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Prepare the task payload.  Adding `unique_id` to the dictionary ensures
    # that consumers can easily identify the task.
    payload = {"unique_id": unique_id, "task_info": task_info}

    try:
        # Prevent uncontrolled resource consumption by checking the queue size
        # before attempting to enqueue.  The `maxsize` attribute of Queue is used
        # as the upper bound; if it's 0, the queue size is infinite.
        maxsize = task_queue.maxsize
        if maxsize > 0 and task_queue.qsize() >= maxsize:
            return False

        # Use a short timeout to avoid blocking indefinitely.
        task_queue.put(payload, block=True, timeout=0.1)
    except (queue.Full, queue.Empty):
        # Queue is full or operation timed out; return False to signal failure.
        return False
    except Exception:
        # Catch any unexpected exception without propagating it.
        return False

    return True