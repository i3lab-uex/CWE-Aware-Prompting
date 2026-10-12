#!/usr/bin/env python3
"""
Utility module for task queue management in a parallel processing system.
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict

# Configure basic logger (in real applications this would be more elaborate)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Global task queue with a reasonable maximum size to mitigate CWE-770
MAX_QUEUE_SIZE = 10_000   # Adjust as appropriate for your system
task_queue: Queue[Dict[str, Dict]] = Queue(maxsize=MAX_QUEUE_SIZE)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global task queue.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        True if the task was successfully enqueued, False otherwise.
    """
    # Validate inputs
    if not isinstance(unique_id, str) or not unique_id:
        logger.warning("enqueue_task called with invalid unique_id: %r", unique_id)
        return False
    if not isinstance(task_info, dict):
        logger.warning("enqueue_task called with invalid task_info type: %r", type(task_info))
        return False

    # Prepare the payload
    task_payload = {"id": unique_id, "info": task_info}

    try:
        # Non-blocking put to avoid indefinite waiting
        task_queue.put_nowait(task_payload)
    except Full:
        # Queue is full; log and return failure
        logger.error("Task queue is full. Unable to enqueue task %s.", unique_id)
        return False
    except Exception as exc:  # pragma: no cover
        # Unexpected errors should not propagate; log and return False
        logger.exception("Unexpected error enqueuing task %s: %s", unique_id, exc)
        return False

    logger.debug("Enqueued task %s successfully.", unique_id)
    return True