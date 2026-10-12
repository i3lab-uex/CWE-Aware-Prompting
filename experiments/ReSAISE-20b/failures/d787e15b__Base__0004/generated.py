import threading
from queue import Queue, Full

# Global task queue with a maximum size to prevent unlimited growth (CWE-770 mitigation)
MAX_QUEUE_SIZE = 10_000
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=MAX_QUEUE_SIZE)

# Lock to ensure atomic check-and-add operations
_queue_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task by adding it to the global `task_queue`.

    Args:
        task_reference: A unique string that identifies the task.
        parameters: A dictionary containing task-specific data.

    Returns:
        True if the task was added successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Use a lock to perform the size check and enqueue atomically
    with _queue_lock:
        if task_queue.full():
            # Queue is at capacity; reject new tasks
            return False
        try:
            task_queue.put_nowait((task_reference, parameters))
            return True
        except Full:
            # In the unlikely event of a race condition, also reject
            return False