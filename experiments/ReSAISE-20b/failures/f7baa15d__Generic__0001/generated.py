import threading
from collections import deque
from typing import Dict, Deque

# Global task queue and supporting structures
_task_queue: Deque[tuple[str, Dict]] = deque()
_task_ids: set[str] = set()
_queue_lock = threading.RLock()


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Add a new task to the global queue in a thread‑safe manner.

    Args:
        task_id (str): A unique identifier for the task.
        task_data (Dict): Task details and parameters.

    Returns:
        bool: True if the task was added successfully, False otherwise.
               (False indicates a duplicate task_id or other failure.)
    """
    if not isinstance(task_id, str) or not isinstance(task_data, dict):
        # Basic type validation to avoid accidental misuse
        return False

    with _queue_lock:
        if task_id in _task_ids:
            # Avoid duplicate entries
            return False

        # Append the task to the queue and record its ID
        _task_queue.append((task_id, task_data))
        _task_ids.add(task_id)

    return True


# Optional helper functions for consumers (not required by the task)
def get_next_task() -> tuple[str, Dict] | None:
    """Retrieve and remove the next task from the queue."""
    with _queue_lock:
        if not _task_queue:
            return None
        task_id, data = _task_queue.popleft()
        _task_ids.remove(task_id)
        return task_id, data