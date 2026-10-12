# -*- coding: utf-8 -*-
"""
Module providing a thread‑safe helper for adding tasks to a global queue.
"""

import logging
from queue import Queue, Full

# Global task queue.  The maxsize should be set according to system limits
# to mitigate CWE‑770 (unbounded resource allocation).  A reasonable default
# is provided but can be overridden by the consumer.
task_queue: Queue = Queue(maxsize=1000)

logger = logging.getLogger(__name__)


def insert_task_to_queue(job_id: str, job_data: dict) -> bool:
    """
    Safely insert a task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing task parameters and related metadata.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Basic validation to avoid corrupt entries
    if not isinstance(job_id, str) or not job_id:
        logger.debug("insert_task_to_queue: invalid job_id %r", job_id)
        return False

    if not isinstance(job_data, dict):
        logger.debug("insert_task_to_queue: job_data is not a dict")
        return False

    task = {"job_id": job_id, "job_data": job_data}

    try:
        # The queue's maxsize limits the number of pending tasks,
        # protecting against resource exhaustion.
        task_queue.put(task, block=False)
    except Full:
        logger.warning(
            "insert_task_to_queue: queue is full; task %s not added",
            job_id,
        )
        return False
    except Exception as exc:  # pragma: no cover
        logger.exception(
            "insert_task_to_queue: unexpected error while adding task %s: %s",
            job_id,
            exc,
        )
        return False

    logger.debug("insert_task_to_queue: task %s queued successfully", job_id)
    return True