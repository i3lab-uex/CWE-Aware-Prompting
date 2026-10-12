#!/usr/bin/env python3
"""
Utility for adding tasks to a global task queue in a parallel processing system.

The implementation safeguards against uncontrolled resource consumption
(CWE‑400) by respecting the queue's maximum size and handling exceptions
gracefully.
"""

from __future__ import annotations

import logging
from queue import Queue, Full, Empty
from typing import Dict

# Configure a basic logger for debugging purposes.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Global task queue.
# The `maxsize` argument defines the upper bound of queued tasks to prevent
# memory exhaustion. A value of 0 indicates infinite size, so we set a sane
# default (e.g., 10000) to mitigate CWE‑400 risks.
TASK_QUEUE_MAXSIZE: int = 10_000
task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=TASK_QUEUE_MAXSIZE)


def push_task_to_queue(task_uid: str, task_info: Dict) -> bool:
    """
    Insert a new task into the global queue.

    Parameters
    ----------
    task_uid : str
        A unique identifier for the task.
    task_info : dict
        Dictionary containing task parameters and metadata.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, ``False`` otherwise.

    Notes
    -----
    * The function never raises an exception; failures are logged and a
      ``False`` value is returned.
    * If the queue has reached its maximum size, the task is rejected to
      avoid uncontrolled resource consumption.
    """
    if not isinstance(task_uid, str):
        logger.warning("task_uid must be a string; got %r", type(task_uid))
        return False
    if not isinstance(task_info, dict):
        logger.warning("task_info must be a dict; got %r", type(task_info))
        return False

    try:
        # Use put_nowait to avoid blocking; if the queue is full, a Full
        # exception will be raised and we can handle it gracefully.
        task_queue.put_nowait((task_uid, task_info))
        logger.debug("Task %s queued successfully.", task_uid)
        return True
    except Full:
        logger.warning(
            "Failed to enqueue task %s: queue is full (maxsize=%d).",
            task_uid,
            TASK_QUEUE_MAXSIZE,
        )
        return False
    except Exception as exc:  # pragma: no cover
        logger.exception("Unexpected error while enqueuing task %s: %s", task_uid, exc)
        return False