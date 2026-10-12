import queue
from typing import Dict

# Global task queue with a reasonable size limit to avoid uncontrolled resource consumption (CWE-400).
# Adjust `maxsize` as appropriate for the application.
task_queue: queue.Queue = queue.Queue(maxsize=1000)

def register_new_task(task_reference: str, parameters: Dict) -> bool:
    """
    Register a new task into the global task queue.

    Args:
        task_reference (str): A unique identifier for the task.
        parameters (dict): Task-specific data.

    Returns:
        bool: True if the task was enqueued successfully, False otherwise.
    """
    # Basic validation to avoid accidental misuse
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Attempt to enqueue the task without blocking.
    try:
        task_queue.put_nowait((task_reference, parameters.copy()))
        return True
    except queue.Full:
        # Queue is full; reject the task to prevent resource exhaustion.
        return False