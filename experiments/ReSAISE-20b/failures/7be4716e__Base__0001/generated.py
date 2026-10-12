# enqueue_task.py

"""
Utility to safely add tasks to a global multiprocessing queue.
Implements basic size checks to mitigate CWE‑770 (resource exhaustion).
"""

import logging
from multiprocessing import Queue

# Configure a module‑level logger. In real deployments, this could be
# configured by the application using `logging.config`.
logger = logging.getLogger(__name__)
if not logger.handlers:
    # Avoid duplicate handlers if this module is imported multiple times
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Global task queue used by the system. It is intentionally created with
# a maxsize to guard against unlimited growth.
TASK_QUEUE_MAXSIZE = 1000  # Adjust as appropriate for the environment
task_queue: Queue = Queue(maxsize=TASK_QUEUE_MAXSIZE)


def enqueue_task(unique_id: str, task_info: dict) -> bool:
    """
    Safely add a task to the global task queue.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing all relevant information for the task.

    Returns
    -------
    bool
        True if the task was enqueued successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(unique_id, str):
        logger.error("enqueue_task: unique_id must be a string")
        return False
    if not isinstance(task_info, dict):
        logger.error("enqueue_task: task_info must be a dictionary")
        return False

    # Check queue capacity to prevent unbounded growth
    try:
        current_size = task_queue.qsize()
    except NotImplementedError:
        # On some platforms qsize() is not reliable; we fall back to a best‑effort approach
        current_size = None

    if current_size is not None and current_size >= TASK_QUEUE_MAXSIZE:
        logger.warning(
            f"enqueue_task: queue size {current_size} reached max {TASK_QUEUE_MAXSIZE}. "
            "Task not enqueued."
        )
        return False

    # Prepare the payload
    task_payload = {
        "unique_id": unique_id,
        "task_info": task_info,
    }

    try:
        # The put() call will block if the queue is full; using a timeout prevents
        # indefinite blocking in edge cases.
        task_queue.put(task_payload, block=False)
    except Exception as exc:
        logger.exception("enqueue_task: failed to enqueue task")
        return False

    logger.debug(f"Task {unique_id} enqueued successfully.")
    return True