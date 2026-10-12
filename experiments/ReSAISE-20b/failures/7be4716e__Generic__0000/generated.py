#!/usr/bin/env python3
"""
Utility for inserting tasks into a shared queue.

This module defines :func:`enqueue_task`, which safely enqueues a task
identified by ``unique_id`` together with its associated information
dictionary into a globally shared :class:`queue.Queue` instance named
``task_queue``.

The function returns ``True`` on success and ``False`` if the operation
fails for any reason (e.g. queue full or runtime errors).  No exception
is propagated to callers.
"""

import logging
from typing import Dict

try:
    # The shared queue should be defined elsewhere in the application.
    from task_queue_module import task_queue  # type: ignore
except Exception:
    # Fallback for demonstration/testing purposes.
    import queue
    task_queue = queue.Queue(maxsize=0)  # unbounded

logger = logging.getLogger(__name__)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Enqueue a new task into the global ``task_queue``.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    - The function does **not** raise exceptions; failures are logged and
      a ``False`` value is returned.
    - If the queue is bounded and full, :meth:`queue.Full` will be caught
      and handled gracefully.
    """
    try:
        # We put the task as a tuple (unique_id, task_info) to preserve
        # uniqueness and data together.
        task_queue.put((unique_id, task_info), block=False)
    except queue.Full:
        logger.warning("Task queue is full. Failed to enqueue task %s.", unique_id)
        return False
    except Exception as exc:  # pragma: no cover - defensive catch-all
        logger.exception("Unexpected error while enqueuing task %s: %s", unique_id, exc)
        return False

    logger.debug("Task %s enqueued successfully.", unique_id)
    return True