import queue
import logging
from typing import Dict

# Configure a basic logger for debugging purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Global task queue; if it doesn't exist, create one
try:
    # If the global is already defined elsewhere, use it.
    task_queue  # noqa: F821
except NameError:
    task_queue = queue.Queue()


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        A dictionary containing all relevant information about the task.

    Returns
    -------
    bool
        True if the task was successfully added to the queue,
        False otherwise.
    """
    # Basic validation
    if not isinstance(unique_id, str) or not unique_id:
        logging.warning("enqueue_task: invalid unique_id '%s'", unique_id)
        return False
    if not isinstance(task_info, dict):
        logging.warning("enqueue_task: task_info must be a dict")
        return False

    # Package the task
    task_payload = {"id": unique_id, "info": task_info}

    try:
        # Use put_nowait to avoid blocking if the queue is full
        task_queue.put_nowait(task_payload)
    except queue.Full:
        logging.error("enqueue_task: queue is full, cannot add task '%s'", unique_id)
        return False
    except Exception as exc:
        # Catch-all for unforeseen errors
        logging.exception("enqueue_task: unexpected error adding task '%s': %s", unique_id, exc)
        return False

    logging.info("enqueue_task: task '%s' added successfully", unique_id)
    return True