# register_new_task.py

import threading
from queue import Queue, Full

# Global task queue (thread‑safe)
task_queue: Queue[tuple[str, dict]] = Queue(maxsize=0)  # unlimited size

# Lock to ensure the uniqueness of task_reference if needed
_task_lock = threading.Lock()
_existing_references: set[str] = set()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global task queue.

    Args:
        task_reference (str): Unique identifier for the task.
        parameters (dict): Task-specific parameters.

    Returns:
        bool: True if the task was added successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Ensure the task reference is unique
    with _task_lock:
        if task_reference in _existing_references:
            return False  # duplicate reference
        _existing_references.add(task_reference)

    try:
        task_queue.put_nowait((task_reference, parameters))
    except Full:  # unlikely with unlimited size but defensive
        with _task_lock:
            _existing_references.remove(task_reference)
        return False

    return True