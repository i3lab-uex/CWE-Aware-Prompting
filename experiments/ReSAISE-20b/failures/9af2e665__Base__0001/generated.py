import queue
from typing import Dict, Any

# Global task queue with a reasonable size limit to avoid unbounded growth.
# The limit can be tuned according to system resources; 10_000 is a common safe default.
task_queue: queue.Queue = queue.Queue(maxsize=10_000)


def push_task_to_queue(task_uid: str, task_info: Dict[str, Any]) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    task_uid : str
        Unique identifier for the task. Must be a non-empty string.
    task_info : dict
        Dictionary containing task details, parameters, and metadata.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic input validation
    if not isinstance(task_uid, str) or not task_uid:
        return False
    if not isinstance(task_info, dict):
        return False

    # Prepare the payload to enqueue
    task_payload = {"uid": task_uid, "info": task_info}

    try:
        # Attempt to enqueue with a short timeout to avoid blocking indefinitely.
        task_queue.put(task_payload, block=True, timeout=0.1)
    except queue.Full:
        # Queue is full; do not block further.
        return False
    except Exception:
        # Catch-all for unexpected issues; do not raise to callers.
        return False

    return True