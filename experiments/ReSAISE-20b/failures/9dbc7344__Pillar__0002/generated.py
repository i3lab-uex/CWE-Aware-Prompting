import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue = Queue(maxsize=1000)  # Adjust size as needed

# Lock to guard the set of task identifiers (optional, for uniqueness)
_task_ids_lock = threading.Lock()
_enqueued_ids = set()

def insert_task_to_queue(task_identifier: str, task_content: dict) -> bool:
    """
    Append a new task to the global queue.

    Parameters
    ----------
    task_identifier : str
        Unique identifier for the task.
    task_content : dict
        Parameters and details of the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(task_identifier, str) or not task_identifier:
        return False
    if not isinstance(task_content, dict):
        return False

    # Ensure the identifier is unique in the current queue
    with _task_ids_lock:
        if task_identifier in _enqueued_ids:
            return False
        # Reserve the identifier
        _enqueued_ids.add(task_identifier)

    try:
        task_queue.put_nowait((task_identifier, task_content))
    except Full:
        # Queue is full; release the identifier reservation
        with _task_ids_lock:
            _enqueued_ids.discard(task_identifier)
        return False
    except Exception:
        # Unexpected error; release the identifier reservation
        with _task_ids_lock:
            _enqueued_ids.discard(task_identifier)
        return False

    # Successful enqueue
    return True