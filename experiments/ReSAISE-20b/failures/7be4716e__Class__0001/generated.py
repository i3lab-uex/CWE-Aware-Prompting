import queue
from typing import Dict

# Global task queue used by the parallel processing system.
# A bounded size is set to avoid uncontrolled resource consumption (CWE-400).
task_queue: queue.Queue = queue.Queue(maxsize=1000)  # adjust size as needed


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Safely add a new task to the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and other relevant data.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Validate inputs early to avoid unnecessary queue operations
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Construct the task payload.  We keep it minimal to reduce memory usage.
    task_payload = {
        "id": unique_id,
        "info": task_info,
    }

    try:
        # `put_nowait` ensures we do not block indefinitely; if the queue is full
        # we simply return False to indicate failure.
        task_queue.put_nowait(task_payload)
    except queue.Full:
        # The queue is at its maximum capacity; we avoid allocating more resources.
        return False
    except Exception:
        # Any unexpected exception is caught to prevent crashing the caller.
        return False

    return True