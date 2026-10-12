#!/usr/bin/env python3
"""
Utility for inserting tasks into a shared queue in a parallel processing system.
"""

from __future__ import annotations

import logging
from queue import Queue, Full, Empty
from typing import Dict

# Configure module level logger (users may configure root logger)
_logger = logging.getLogger(__name__)

# Global task queue used by the system.  In a real application this would
# be instantiated elsewhere and imported here, but for completeness we create it.
task_queue: Queue = Queue()


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        A unique string identifier for the task.
    job_data : dict
        Dictionary containing the task's parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, ``False`` otherwise.

    Notes
    -----
    * The function validates input types to avoid accidental misuse.
    * It uses ``put_nowait`` to prevent blocking; if the queue is full, it
      logs a warning and returns ``False``.
    * All exceptions are caught to guarantee that the function never raises
      and always returns a boolean.
    """
    # Basic type checks – defensive programming to avoid silent failures
    if not isinstance(job_id, str):
        _logger.debug("insert_task_to_queue: job_id is not a string")
        return False
    if not isinstance(job_data, dict):
        _logger.debug("insert_task_to_queue: job_data is not a dict")
        return False

    task_payload = {"job_id": job_id, "job_data": job_data}

    try:
        # Non-blocking put; if the queue is full, we consider this a failure
        task_queue.put_nowait(task_payload)
    except Full:
        _logger.warning(
            "insert_task_to_queue: task queue is full; cannot enqueue job %s",
            job_id,
        )
        return False
    except Exception as exc:  # pragma: no cover
        # Catch any unforeseen exception to maintain the contract of never raising
        _logger.error(
            "insert_task_to_queue: unexpected error while enqueueing job %s: %s",
            job_id,
            exc,
        )
        return False

    _logger.debug("insert_task_to_queue: enqueued job %s successfully", job_id)
    return True