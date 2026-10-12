import threading
from collections import deque
from typing import Dict

# Global task queue and its lock
MAX_QUEUE_SIZE = 1000          # Maximum number of tasks allowed in the queue
_task_queue_lock = threading.Lock()
task_queue: deque[tuple[str, Dict]] = deque()

def queue_new_task(unique_task_id: str, task_info: Dict) -> bool:
    """
    Append a new task to the global queue in a thread‑safe manner.

    Args:
        unique_task_id (str): A unique identifier for the task.
        task_info (Dict): Dictionary containing task parameters.

    Returns:
        bool: True if the task was enqueued, False otherwise (e.g., queue full).
    """
    # Validate input types
    if not isinstance(unique_task_id, str) or not isinstance(task_info, dict):
        return False

    with _task_queue_lock:
        # Enforce maximum queue size to mitigate uncontrolled resource consumption
        if len(task_queue) >= MAX_QUEUE_SIZE:
            return False

        # Append the task as a tuple (id, info) to preserve uniqueness and data
        task_queue.append((unique_task_id, task_info))
    return True