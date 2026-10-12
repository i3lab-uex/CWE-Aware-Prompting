# -*- coding: utf-8 -*-

"""
Module providing a safe task enqueueing mechanism for a shared queue.
"""

import logging
from queue import Queue, Full

# Configure module level logger
_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())

# Global task queue used by the system
task_queue: Queue = Queue(maxsize=1000)  # Adjust maxsize as needed

def enqueue_task(unique_id: str, task_info: dict) -> bool:
    """
    Safely add a new task to the global task queue.

    Args:
        unique_id (str): A unique identifier for the task.
        task_info (dict): Dictionary containing task parameters and metadata.

    Returns:
        bool: True if the task was successfully enqueued, False otherwise.
    """
    # Basic validation
    if not isinstance(unique_id, str) or not unique_id:
        _logger.debug("enqueue_task: invalid unique_id '%s'", unique_id)
        return False
    if not isinstance(task_info, dict):
        _logger.debug("enqueue_task: task_info is not a dict")
        return False

    # Compose the payload
    payload = {
        "id": unique_id,
        "info": task_info,
    }

    try:
        # Non-blocking put to avoid hanging if queue is full
        task_queue.put_nowait(payload)
    except Full:
        _logger.warning("enqueue_task: queue is full; task '%s' rejected", unique_id)
        return False
    except Exception as exc:  # Catch unforeseen exceptions to avoid crashing the caller
        _logger.exception("enqueue_task: unexpected error while enqueuing task '%s': %s", unique_id, exc)
        return False

    _logger.debug("enqueue_task: task '%s' enqueued successfully", unique_id)
    return True