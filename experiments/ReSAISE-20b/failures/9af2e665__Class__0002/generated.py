import threading
from queue import Queue, Full

# Global task queue with a bounded size to prevent uncontrolled resource consumption.
TASK_QUEUE_MAXSIZE = 1000  # Adjust based on system capacity
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=TASK_QUEUE_MAXSIZE)

# Lock to protect concurrent access to the queue size check and put operation.
_queue_lock = threading.Lock()


def push_task_to_queue(task_uid: str, task_info: dict) -> bool:
    """
    Safely push a new task into the global task queue.

    Args:
        task_uid (str): Unique identifier for the task.
        task_info (dict): Dictionary containing task details and parameters.

    Returns:
        bool: True if the task was successfully added, False otherwise.
    """
    # Validate input types
    if not isinstance(task_uid, str) or not isinstance(task_info, dict):
        return False

    with _queue_lock:
        if task_queue.full():
            # Queue is at capacity; do not block or raise.
            return False
        try:
            task_queue.put_nowait((task_uid, task_info))
            return True
        except Full:
            # Rare race condition: queue became full after the check.
            return False
        except Exception:
            # Catch any unexpected exception to avoid crashing the system.
            return False