# -*- coding: utf-8 -*-
"""
Utility for enqueuing tasks into a global task queue.
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict, Optional

# Global task queue; created lazily if not present.
try:
    # If another module has already defined it, use that one.
    task_queue  # type: ignore[name-defined]
except NameError:
    task_queue = Queue(maxsize=0)  # unbounded queue

logger = logging.getLogger(__name__)


def enqueue_task(unique_id: str, task_info: Dict) -> bool:
    """
    Add a new task to the global :data:`task_queue`.

    Parameters
    ----------
    unique_id : str
        A unique identifier for the task. Must be a non-empty string.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was successfully added, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(unique_id, str) or not unique_id.strip():
        logger.warning("enqueue_task: invalid unique_id '%s'", unique_id)
        return False
    if not isinstance(task_info, dict):
        logger.warning("enqueue_task: task_info must be a dict")
        return False

    # Construct the payload
    payload = {"id": unique_id, "info": task_info}

    try:
        # Non-blocking put with a short timeout to avoid deadlocks.
        task_queue.put(payload, block=False)
    except Full:
        logger.error("enqueue_task: queue is full")
        return False
    except Exception as exc:
        # Catch any unforeseen exception to avoid leaking resources.
        logger.exception("enqueue_task: unexpected error %s", exc)
        return False

    return True