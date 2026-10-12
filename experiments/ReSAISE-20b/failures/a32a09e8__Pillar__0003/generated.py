# -*- coding: utf-8 -*-
"""
Utility module for inserting tasks into a shared queue in a parallel
processing system.

The module defines `insert_task_to_queue`, which safely enqueues a task
identified by `job_id` and its associated data `job_data`.  The function
returns ``True`` on success or ``False`` if the task could not be added.
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict

# Configure a module‑level logger; callers may reconfigure as needed.
logger = logging.getLogger(__name__)
if not logger.handlers:
    # Default to console output if no handlers are configured.
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# Global queue instance used by the parallel system.
# In practice, this should be initialized elsewhere in your application
# and imported here.  For demonstration purposes we create a simple queue.
task_queue: Queue = Queue(maxsize=0)  # unlimited size by default


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global ``task_queue``.

    Parameters
    ----------
    job_id : str
        A unique string identifier for the task.
    job_data : dict
        Dictionary containing task details, parameters and other data.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, ``False`` otherwise.

    Notes
    -----
    - The function performs basic type validation to guard against misuse.
    - Any exception raised by the queue (e.g., ``Full``) is caught and logged.
    - The function never propagates exceptions to the caller; it returns
      ``False`` on failure, ensuring callers can handle errors gracefully.
    """
    # Basic input validation
    if not isinstance(job_id, str):
        logger.debug("insert_task_to_queue: job_id is not a string")
        return False
    if not isinstance(job_data, dict):
        logger.debug("insert_task_to_queue: job_data is not a dict")
        return False

    # Optionally, enforce size limits or other business rules here.
    # For example:
    MAX_JOB_DATA_SIZE = 10 * 1024 * 1024  # 10 MB
    try:
        import sys

        if sys.getsizeof(job_data) > MAX_JOB_DATA_SIZE:
            logger.debug("insert_task_to_queue: job_data size exceeds limit")
            return False
    except Exception:
        # In rare cases where sys.getsizeof fails, we simply proceed.
        pass

    try:
        # Queue.put_nowait() raises Full if the queue is bounded and full.
        task_queue.put_nowait((job_id, job_data))
    except Full:
        logger.warning("insert_task_to_queue: queue is full; task not added")
        return False
    except Exception as exc:
        # Catch unexpected exceptions (e.g., serialization errors)
        logger.exception("insert_task_to_queue: unexpected error %s", exc)
        return False

    # If we reach here, the task was enqueued successfully.
    logger.debug("insert_task_to_queue: task %s added to queue", job_id)
    return True