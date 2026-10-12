import queue
from typing import Dict

# Global task queue used by the system.  It is a thread‑safe FIFO queue.
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    task_identifier : str
        A unique string identifying the task.
    task_details : dict
        Parameters and data required to execute the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_details, dict):
        return False

    try:
        # Store as a tuple to keep identifier and details together.
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue is full; cannot accept more tasks.
        return False
    except Exception:
        # Unexpected error during enqueueing
        return False

    return True