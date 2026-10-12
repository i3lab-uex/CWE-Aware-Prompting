import queue
from typing import Dict

# Global task queue. In a real application this would be defined elsewhere,
# but we provide a default instance with a reasonable maximum size to avoid
# uncontrolled resource consumption (CWE‑400).
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=1000)

def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a new task to the global task queue.

    Parameters
    ----------
    identifier : str
        A unique string that identifies the task.
    details : dict
        Parameters and data associated with the task.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation: ensure identifier is a non‑empty string
    if not isinstance(identifier, str) or not identifier:
        return False

    # Ensure details is a dictionary
    if not isinstance(details, dict):
        return False

    try:
        # put_nowait raises queue.Full if the queue is at its maxsize
        task_queue.put_nowait((identifier, details))
    except queue.Full:
        # Queue is full – reject the task to prevent resource exhaustion
        return False

    return True