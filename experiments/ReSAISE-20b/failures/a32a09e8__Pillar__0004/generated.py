# -*- coding: utf-8 -*-

"""
Module providing a thread‑safe helper for inserting tasks into a global queue.
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict

# Global task queue used by the system.
task_queue: Queue = Queue()

def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global ``task_queue``.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing all data required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully queued, otherwise ``False``.

    Notes
    -----
    * The function performs basic type validation to avoid corrupting the queue.
    * ``Queue.put_nowait`` is used to keep the function non‑blocking.  If the queue
      is full an exception will be caught and ``False`` returned.
    * No additional resources are allocated; the function only enqueues a tuple
      containing the provided data, thus avoiding CWE‑664 concerns.
    """
    # Basic type checks
    if not isinstance(job_id, str):
        logging.debug("insert_task_to_queue: job_id is not a string")
        return False
    if not isinstance(job_data, dict):
        logging.debug("insert_task_to_queue: job_data is not a dict")
        return False

    try:
        # Queue is thread‑safe; no explicit lock required.
        task_queue.put_nowait((job_id, job_data))
    except Full:
        # Queue has reached its maxsize (if set); treat as failure.
        logging.warning("insert_task_to_queue: task queue is full")
        return False
    except Exception as exc:
        # Unexpected exception – log and signal failure.
        logging.exception("insert_task_to_queue: unexpected error")
        return False

    return True