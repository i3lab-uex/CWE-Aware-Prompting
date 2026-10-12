import threading
from queue import Queue, Full

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
# Adjust `maxsize` according to system capacity; here we use 1000 as an example.
task_queue: Queue = Queue(maxsize=1000)

# Lock to guard the enqueue operation for additional safety (though Queue is thread‑safe).
_enqueue_lock = threading.Lock()


def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global `task_queue`.

    Args:
        task_identifier (str): Unique string identifier for the task.
        task_content (dict): Dictionary containing task parameters.

    Returns:
        bool: True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    task_item = {"id": task_identifier, "content": task_content}

    try:
        with _enqueue_lock:
            # Attempt to enqueue without blocking; if the queue is full, we return False.
            task_queue.put_nowait(task_item)
        return True
    except Full:
        # Queue reached its maximum size; task cannot be enqueued.
        return False
    except Exception:
        # Any unexpected error is swallowed to satisfy the "Raise: None" requirement.
        return False