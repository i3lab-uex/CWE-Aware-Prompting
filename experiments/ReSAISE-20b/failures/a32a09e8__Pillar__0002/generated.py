# -*- coding: utf-8 -*-
"""
Utility module for inserting tasks into a shared queue in a parallel processing system.
"""

from __future__ import annotations

import logging
import threading
from queue import Queue, Full
from typing import Dict

# Configure a module‑level logger (customize as needed)
_logger = logging.getLogger(__name__)
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)

# Global queue used by the application
_task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=1000)

# Lock to guard the queue insertion for additional safety
_queue_lock = threading.Lock()


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task identified by *job_id* and its associated data into the global
    :data:`_task_queue`.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing task parameters and other metadata.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.
    """
    # Basic validation of inputs
    if not isinstance(job_id, str):
        _logger.debug("job_id is not a string: %r", job_id)
        return False
    if not isinstance(job_data, dict):
        _logger.debug("job_data is not a dict: %r", job_data)
        return False

    # Avoid duplicate entries by checking existing items (optional, not a performance guarantee)
    with _queue_lock:
        # Check for duplicate job_id (linear scan – acceptable if queue size is limited)
        for existing_job_id, _ in list(_task_queue.queue):
            if existing_job_id == job_id:
                _logger.debug("Duplicate job_id detected: %s", job_id)
                return False

        try:
            _task_queue.put_nowait((job_id, job_data))
            _logger.debug("Task queued: %s", job_id)
            return True
        except Full:
            _logger.warning("Queue is full; cannot enqueue task: %s", job_id)
        except Exception as exc:
            _logger.exception("Unexpected error while enqueuing task %s: %s", job_id, exc)

    return False


# Expose the queue for consumers
def get_task_queue() -> Queue[tuple[str, Dict]]:
    """
    Return the global task queue.  Callers should not modify the queue directly.
    """
    return _task_queue