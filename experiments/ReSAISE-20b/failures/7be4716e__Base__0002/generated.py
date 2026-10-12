from queue import Queue, Full

# Global task queue with a reasonable maximum size to avoid unbounded growth.
# Adjust `maxsize` as needed for your system's capacity.
task_queue: Queue = Queue(maxsize=1000)


def enqueue_task(unique_id: str, task_info: dict) -> bool:
    """
    Safely add a new task to the global task queue.

    Args:
        unique_id (str): A unique identifier for the task.
        task_info (dict): Task details, parameters, etc.

    Returns:
        bool: True if the task was enqueued successfully; False otherwise.
    """
    # Construct a tuple or dict that contains both the unique_id and task_info
    task_payload = {"id": unique_id, "info": task_info}

    try:
        # Use put_nowait to avoid blocking; if the queue is full, we fail gracefully.
        task_queue.put_nowait(task_payload)
    except Full:
        # Queue is full; do not raise an exception—just signal failure.
        return False

    return True