# -*- coding: utf-8 -*-

"""
Utility module for inserting tasks into a global multiprocessing queue.

The module defines the `insert_task_to_queue` function, which safely adds a
task represented by a job ID and its associated data to the shared queue.
"""

import logging
from typing import Dict

# Configure module-level logger
logger = logging.getLogger(__name__)

# Global task queue (must be instantiated elsewhere in the application)
task_queue = None  # type: ignore[assignment]

def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a new task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        Unique identifier for the task.
    job_data : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was added successfully, otherwise ``False``.

    Notes
    -----
    - The function does not raise exceptions; any failure is logged and
      a ``False`` return value is used instead.
    - The global `task_queue` must be a thread‑/process‑safe queue
      (e.g., ``multiprocessing.Queue``). It should be initialized before
      calling this function.
    """
    global task_queue

    if task_queue is None:
        logger.error("Global task queue has not been initialized.")
        return False

    if not isinstance(job_id, str):
        logger.error("job_id must be a string. Received: %r", job_id)
        return False

    if not isinstance(job_data, dict):
        logger.error("job_data must be a dictionary. Received: %r", job_data)
        return False

    # Build the task payload
    task_payload = {
        "job_id": job_id,
        "job_data": job_data
    }

    try:
        task_queue.put_nowait(task_payload)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to enqueue task %s: %s", job_id, exc)
        return False

    logger.debug("Task %s enqueued successfully.", job_id)
    return True