# -*- coding: utf-8 -*-
"""
Utility module for inserting tasks into a global queue.
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict

# Configure a module level logger (can be overridden by the main application)
logger = logging.getLogger(__name__)

# Global task queue.  It is created lazily on first import to avoid
# accidental creation of multiple queues in different modules.
_task_queue: Queue | None = None


def get_task_queue() -> Queue:
    """
    Return the global task queue, creating it if necessary.

    The queue is unbounded by default; adjust ``maxsize`` if a bounded
    queue is required.
    """
    global _task_queue
    if _task_queue is None:
        _task_queue = Queue()
    return _task_queue


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a new task into the global queue.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        The data associated with the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully added, ``False`` otherwise.

    Notes
    -----
    * The function is thread‑safe because :class:`queue.Queue` handles
      synchronization internally.
    * No exceptions are propagated; errors are logged and a ``False`` is
      returned instead.
    """
    if not isinstance(job_id, str):
        logger.error("job_id must be a string; got %r", type(job_id))
        return False
    if not isinstance(job_data, dict):
        logger.error("job_data must be a dict; got %r", type(job_data))
        return False

    task_queue = get_task_queue()
    try:
        # Use a tuple to avoid accidental modification of the data after insertion
        task_queue.put((job_id, job_data), block=False)
    except Full:
        logger.warning("Task queue is full; cannot add job_id=%s", job_id)
        return False
    except Exception as exc:  # pragma: no cover – defensive programming
        logger.exception("Unexpected error while inserting task %s: %s", job_id, exc)
        return False

    logger.debug("Inserted task %s into queue.", job_id)
    return True