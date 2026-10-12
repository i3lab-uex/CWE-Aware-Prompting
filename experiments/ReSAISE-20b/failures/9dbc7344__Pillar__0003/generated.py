import threading
from collections import deque
from typing import Dict

# Global task queue and a lock to protect it.
task_queue: deque = deque()
_task_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: Dict) -> bool:
    """
    Append a new task to the global queue.

    Args:
        task_identifier (str): Unique identifier for the task.
        task_content (dict): Dictionary containing task parameters.

    Returns:
        bool: True if the task was enqueued, False otherwise.
    """
    # Basic validation to avoid malformed entries
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_content, dict):
        return False

    # Prevent accidental duplicate identifiers
    with _task_lock:
        for existing_id, _ in task_queue:
            if existing_id == task_identifier:
                return False  # Duplicate ID not allowed

        try:
            task_queue.append((task_identifier, task_content))
            return True
        except Exception:
            # In case of unforeseen errors (e.g., memory exhaustion)
            return False