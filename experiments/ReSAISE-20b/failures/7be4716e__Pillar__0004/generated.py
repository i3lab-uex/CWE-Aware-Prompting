# -*- coding: utf-8 -*-
"""
Utility for adding tasks to a global queue in a parallel processing system.
"""

from __future__ import annotations

import logging
from queue import Queue, Full, Empty
from typing import Dict, Tuple

# Configure a module‑level logger. In real deployments this should be
# configured by the application entry point.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global task queue. In practice this should be instantiated once by the
# application bootstrap code and shared across worker modules.
task_queue: Queue[Tuple[str, Dict]] = Queue(maxsize=1000)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Add a new task to the global ``task_queue``.

    Parameters
    ----------
    unique_id : str
        A unique string identifier for the task.
    task_info : dict
        Dictionary containing task details and parameters.

    Returns
    -------
    bool
        ``True`` if the task was enqueued successfully, otherwise ``False``.

    Notes
    -----
    * The function is non‑blocking; it will not wait if the queue is full.
    * If ``task_queue`` has not been initialized, a warning will be logged
      and the function returns ``False`` to avoid raising an exception.
    """
    # Validate input types (basic runtime check)
    if not isinstance(unique_id, str):
        logger.debug("enqueue_task: unique_id is not a string")
        return False
    if not isinstance(task_info, dict):
        logger.debug("enqueue_task: task_info is not a dict")
        return False

    # Ensure the global queue exists
    if task_queue is None:
        logger.warning("enqueue_task: global task_queue has not been initialized")
        return False

    try:
        # ``block=False`` ensures the call is non‑blocking; if the queue
        # is full, a ``Full`` exception will be raised.
        task_queue.put((unique_id, task_info), block=False)
    except Full:
        logger.warning(
            "enqueue_task: failed to enqueue task '%s' – queue is full",
            unique_id,
        )
        return False
    except Exception as exc:  # pragma: no cover
        logger.exception("enqueue_task: unexpected error while enqueueing task '%s': %s", unique_id, exc)
        return False

    logger.debug("enqueue_task: task '%s' enqueued successfully", unique_id)
    return True