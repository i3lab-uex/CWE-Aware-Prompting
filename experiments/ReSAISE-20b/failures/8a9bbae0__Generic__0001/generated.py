import threading
from queue import Queue, Full

# Global task storage structures
_task_queue = Queue()
_enqueued_ids = set()
_lock = threading.Lock()


def enqueue_task(task_identifier: str, task_details: dict) -> bool:
    """
    Adds a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_details : dict
        Dictionary containing task parameters and specifics.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_details, dict):
        return False

    # Ensure uniqueness of the task identifier
    with _lock:
        if task_identifier in _enqueued_ids:
            return False  # Duplicate ID

        try:
            # Attempt to enqueue the task; use a timeout to avoid indefinite blocking
            _task_queue.put((task_identifier, task_details), block=False)
        except Full:
            return False

        # Record the identifier to prevent duplicates
        _enqueued_ids.add(task_identifier)

    return True


# Expose the queue for consumers (read-only)
def get_task_queue() -> Queue:
    """Return the global task queue."""
    return _task_queue