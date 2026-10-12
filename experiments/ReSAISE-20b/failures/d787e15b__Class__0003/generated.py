import queue
import threading

# Global task queue with a maximum size to prevent uncontrolled resource consumption.
# Adjust MAX_QUEUE_SIZE as appropriate for your environment.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)

# A set to keep track of task references already registered. Protect it with a lock.
_registered_task_refs = set()
_task_lock = threading.Lock()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        Parameters associated with the task.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic type validation (non‑raising).
    if not isinstance(task_reference, str) or not isinstance(parameters, dict):
        return False

    # Ensure uniqueness and thread safety.
    with _task_lock:
        if task_reference in _registered_task_refs:
            return False  # Duplicate reference

        try:
            # Attempt to enqueue without blocking.
            task_queue.put_nowait((task_reference, parameters))
        except queue.Full:
            # Queue is full; cannot accept more tasks.
            return False

        # Record the reference to prevent future duplicates.
        _registered_task_refs.add(task_reference)

    return True