import logging
from threading import RLock

# Configure module‑level logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Global task queue with a fixed maximum size to avoid uncontrolled resource consumption
MAX_QUEUE_SIZE = 10_000   # adjust as appropriate for your environment

# Use a re‑entrant lock to guard concurrent access
_queue_lock = RLock()
_task_queue = []

# Keep a set of registered task identifiers for quick duplicate checks
_registered_ids = set()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        Unique identifier for the task.
    parameters : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(task_reference, str) or not task_reference:
        logger.debug("Invalid task_reference: %r", task_reference)
        return False

    if not isinstance(parameters, dict):
        logger.debug("Parameters must be a dictionary; got %r", type(parameters))
        return False

    with _queue_lock:
        # Reject duplicate task identifiers
        if task_reference in _registered_ids:
            logger.debug("Duplicate task_reference detected: %s", task_reference)
            return False

        # Enforce maximum queue size to mitigate CWE‑400
        if len(_task_queue) >= MAX_QUEUE_SIZE:
            logger.warning("Task queue is full; cannot register new task %s", task_reference)
            return False

        # Append the task to the queue
        _task_queue.append((task_reference, parameters))
        _registered_ids.add(task_reference)
        logger.debug("Task %s registered successfully", task_reference)

    return True