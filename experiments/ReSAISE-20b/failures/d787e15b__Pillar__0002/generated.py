import queue
from typing import Dict

# Global task queue used by the application.
task_queue: queue.Queue = queue.Queue()

def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        The parameters associated with the task.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation: ensure task_reference is a non‑empty string
    if not isinstance(task_reference, str) or not task_reference:
        return False

    # Basic validation: parameters must be a dictionary
    if not isinstance(parameters, dict):
        return False

    # Construct the task entry.  The tuple format keeps it simple
    task_entry = (task_reference, parameters)

    try:
        # The Queue class is thread‑safe for put/get operations.
        task_queue.put(task_entry, block=False)
    except queue.Full:
        # Queue is full; cannot accept new tasks at this time.
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking resources.
        return False

    return True