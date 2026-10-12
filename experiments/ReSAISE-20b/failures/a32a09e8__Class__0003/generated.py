import logging
from queue import Queue, Full

# Global task queue (maxsize can be tuned to avoid resource exhaustion)
task_queue = Queue(maxsize=1000)

# Configure logging for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

def insert_task_to_queue(job_id: str, job_data: dict) -> bool:
    """
    Safely insert a task into the global task queue.

    Args:
        job_id (str): Unique identifier for the task.
        job_data (dict): Dictionary containing task details and parameters.

    Returns:
        bool: True if the task was successfully added, False otherwise.
    """
    # Basic validation
    if not isinstance(job_id, str) or not job_id:
        logging.warning("Invalid job_id: %r", job_id)
        return False
    if not isinstance(job_data, dict):
        logging.warning("job_data must be a dictionary; got %r", type(job_data))
        return False

    # Attempt to add the task with a short timeout to avoid blocking indefinitely.
    try:
        task_queue.put((job_id, job_data), block=True, timeout=1)
        logging.debug("Task %s enqueued successfully.", job_id)
        return True
    except Full:
        # Queue is full; log and return failure to prevent uncontrolled resource consumption.
        logging.warning("Task queue is full. Unable to enqueue job_id: %s", job_id)
        return False
    except Exception as exc:
        # Catch-all for unexpected errors; log and fail gracefully.
        logging.error("Unexpected error while enqueuing job_id %s: %s", job_id, exc)
        return False