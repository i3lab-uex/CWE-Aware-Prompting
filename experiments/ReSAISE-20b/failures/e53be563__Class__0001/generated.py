import queue
from typing import Dict

# Global task queue.  If it already exists, this will simply reference it.
# The maxsize is set to a reasonable default (e.g., 1000) to prevent uncontrolled
# resource consumption.  Adjust as needed for your application.
task_queue: queue.Queue = queue.Queue(maxsize=1000)

def push_task(uid: str, data: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    uid : str
        Unique identifier for the task.
    data : dict
        Dictionary containing task parameters and details.

    Returns
    -------
    bool
        True if the task was added successfully; False otherwise.
    """
    # Validate inputs (basic sanity checks)
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    task = {"uid": uid, "data": data}

    try:
        # `block=False` ensures we do not block indefinitely if the queue is full.
        task_queue.put_nowait(task)
    except queue.Full:
        # Queue has reached its maxsize; do not add the task.
        return False
    except Exception:
        # Catch any unforeseen exception and fail gracefully.
        return False

    return True