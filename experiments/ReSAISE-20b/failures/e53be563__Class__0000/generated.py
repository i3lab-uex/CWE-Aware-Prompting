# -*- coding: utf-8 -*-
"""
Thread‑safe task push utility.

This module provides a single function, :func:`push_task`, which
adds a task to a globally shared queue.  The queue is bounded
(`maxsize=1000`) to guard against uncontrolled resource consumption
(CWE‑400).  The function returns ``True`` if the task was enqueued
successfully, otherwise ``False`` (e.g., when the queue is full).
"""

from __future__ import annotations

import logging
from queue import Queue, Full
from typing import Dict

# Configure a module‑level logger (no propagation to avoid duplicate logs)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Global task queue – bounded to prevent uncontrolled growth.
# The size can be tuned as needed; 1000 is a reasonable default for
# many applications. Adjust with environment variables or config files if required.
task_queue: Queue[tuple[str, Dict]] = Queue(maxsize=1000)


def push_task(uid: str, data: Dict) -> bool:
    """
    Safely add a task to the global :data:`task_queue`.

    Parameters
    ----------
    uid : str
        Unique identifier for the task. Must be a non‑empty string.
    data : dict
        Dictionary containing task parameters.

    Returns
    -------
    bool
        ``True`` if the task was enqueued, ``False`` otherwise.

    Notes
    -----
    - The function does **not** raise exceptions; failures are logged
      and a ``False`` return value is provided.
    - The queue is bounded; if it reaches capacity, the task will not
      be added and ``False`` is returned.
    - The function validates inputs minimally to guard against
      accidental misuse (e.g., empty UID or non‑dict data).

    Examples
    --------
    >>> push_task("job-1", {"action": "process", "payload": [1, 2, 3]})
    True
    """
    # Basic input validation
    if not isinstance(uid, str) or not uid:
        logger.warning("push_task called with invalid UID: %r", uid)
        return False
    if not isinstance(data, dict):
        logger.warning("push_task called with non‑dict data: %r", data)
        return False

    try:
        # ``put_nowait`` raises Full if the queue is at capacity.
        task_queue.put_nowait((uid, data))
    except Full:
        logger.error("Task queue is full. Unable to enqueue task %s.", uid)
        return False
    except Exception as exc:  # pragma: no cover - defensive programming
        logger.exception("Unexpected error while enqueuing task %s: %s", uid, exc)
        return False

    logger.debug("Task %s enqueued successfully.", uid)
    return True