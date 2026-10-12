import queue
from typing import Dict

# Global task queue used by the system.
task_queue: queue.Queue = queue.Queue()


def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique identifier for the task.
    parameters : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue, False otherwise.
    """
    try:
        # Pack the task into a tuple for storage.  The queue is thread‑safe.
        task_queue.put((task_reference, parameters), block=False)
        return True
    except queue.Full:
        # Queue is full; the task could not be added.
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking the task queue state.
        return False