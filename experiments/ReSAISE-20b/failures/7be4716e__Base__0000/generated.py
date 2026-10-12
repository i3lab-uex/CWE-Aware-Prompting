import queue
from typing import Dict

# Global task queue (should be created elsewhere in the application)
# Example: task_queue = queue.Queue(maxsize=1000)
task_queue: queue.Queue = None  # placeholder; replace with actual instance

def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Safely add a new task to the global `task_queue`.

    Args:
        unique_id (str): A unique identifier for the task.
        task_info (dict): Detailed information about the task.

    Returns:
        bool: True if the task was enqueued successfully, False otherwise.
    """
    global task_queue

    # Basic validation
    if not isinstance(unique_id, str) or not unique_id:
        return False
    if not isinstance(task_info, dict):
        return False

    # Ensure the global queue exists
    if task_queue is None:
        return False

    try:
        # Attempt to put the task without blocking; if full, fail gracefully
        task_queue.put((unique_id, task_info), block=False)
    except queue.Full:
        # Queue has reached its maximum capacity
        return False
    except Exception:
        # Catch any unexpected exception to avoid propagating errors
        return False

    return True