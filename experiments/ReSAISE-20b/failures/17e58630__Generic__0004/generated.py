import queue

# Global task queue used by the system.
# Using an unbounded FIFO queue for simplicity; adjust maxsize if needed.
task_queue: queue.Queue[tuple[str, dict]] = queue.Queue()

def enqueue_task(identifier: str, details: dict) -> bool:
    """
    Add a new task to the global task queue.

    Args:
        identifier: A unique string that identifies the task.
        details:   A dictionary containing task parameters.

    Returns:
        bool: True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(identifier, str) or not identifier:
        return False
    if not isinstance(details, dict):
        return False

    try:
        # Use put_nowait to avoid blocking in a full queue scenario.
        task_queue.put_nowait((identifier, details))
        return True
    except queue.Full:
        # Queue is full; task cannot be enqueued.
        return False