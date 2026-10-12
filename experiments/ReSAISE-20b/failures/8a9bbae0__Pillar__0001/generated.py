import queue
from typing import Dict

# Global task queue.  A FIFO queue is suitable for most task‑processing scenarios.
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue()


def enqueue_task(task_identifier: str, task_details: Dict) -> bool:
    """
    Safely add a new task to the global `task_queue`.

    Parameters
    ----------
    task_identifier : str
        A unique string identifier for the task.
    task_details : dict
        Dictionary containing all parameters required to execute the task.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation: ensure types are correct and values are non‑empty
    if not isinstance(task_identifier, str) or not task_identifier:
        return False

    if not isinstance(task_details, dict):
        return False

    # Queue size limit can be applied to prevent resource exhaustion.
    # Here we allow an unbounded queue; adjust if necessary.
    try:
        task_queue.put_nowait((task_identifier, task_details))
    except queue.Full:  # pragma: no cover
        return False

    return True