import queue
from typing import Dict

# Global task queue used by the system
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Append a new task to the global task queue.

    Args:
        task_identifier (str): A unique string identifier for the task.
        task_details (dict): A dictionary containing task specifics and parameters.

    Returns:
        bool: True if the task was successfully enqueued, False otherwise.
    """
    # Basic input validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_details, dict):
        return False

    try:
        # Use a tuple to store the identifier and details together
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:
        # Queue is full (unlikely with default unbounded size)
        return False
    except Exception:
        # Catch-all for unexpected errors, but do not raise
        return False

    return True