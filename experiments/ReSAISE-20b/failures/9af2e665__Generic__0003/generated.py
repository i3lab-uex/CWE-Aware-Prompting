import queue
from typing import Dict, Any

# Global task queue used by the system.  It must be created
# before any calls to `push_task_to_queue`.
task_queue: queue.Queue[Dict[str, Any]] = queue.Queue()


def push_task_to_queue(task_uid: str, task_info: Dict[str, Any]) -> bool:
    """
    Add a new task to the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued,
        otherwise ``False``.
    """
    # Basic validation: ensure arguments are of expected type
    if not isinstance(task_uid, str) or not task_uid:
        return False

    if not isinstance(task_info, dict):
        return False

    # Compose the task payload.  Using a tuple keeps the data
    # immutable for queue consumers and reduces accidental mutation.
    payload = (task_uid, task_info)

    try:
        # `queue.Queue.put_nowait()` raises ``queue.Full`` if the queue
        # is bounded and full.  Using `put_nowait` keeps the function
        # non-blocking, which is suitable for a push operation that
        # should not delay the caller.
        task_queue.put_nowait(payload)
    except queue.Full:
        # The queue is full; we cannot accept the task at this time.
        return False
    except Exception:
        # Catch any unforeseen exception to keep the API contract clean.
        return False

    return True