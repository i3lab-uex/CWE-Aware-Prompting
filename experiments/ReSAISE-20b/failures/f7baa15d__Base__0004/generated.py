import queue
from typing import Dict

# Define a global task queue with a reasonable maximum size to prevent resource exhaustion.
# Adjust MAX_QUEUE_SIZE based on your system's capacity and expected workload.
MAX_QUEUE_SIZE = 10_000
task_queue: queue.Queue[tuple[str, Dict]] = queue.Queue(maxsize=MAX_QUEUE_SIZE)


def add_task_to_queue(task_id: str, task_data: Dict) -> bool:
    """
    Add a new task to the global queue for later processing.

    Parameters
    ----------
    task_id : str
        A unique identifier for the task.
    task_data : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False if the queue is full and the task could not be queued.

    Notes
    -----
    * The function uses `put_nowait` to avoid blocking the caller.
    * If the queue has reached its maximum size, a `queue.Full` exception
      is caught and False is returned.
    * This approach mitigates CWE‑770 by limiting the number of queued tasks
      that can be allocated at any time.
    """
    try:
        task_queue.put_nowait((task_id, task_data))
        return True
    except queue.Full:
        # Queue is full; the caller can decide to retry later or handle overflow.
        return False