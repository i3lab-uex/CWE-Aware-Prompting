# -*- coding: utf-8 -*-
"""
A small utility for inserting tasks into a shared queue in a parallel
processing environment.  The implementation guards against unbounded
resource consumption (CWE‑770) by respecting the queue's maximum size.
"""

from __future__ import annotations

import logging
from typing import Any, Dict
from queue import Queue, Full

# Configure a module‑level logger; users can adjust logging elsewhere
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Global task queue; in a real system this would be created elsewhere
# and imported.  We set a modest default maxsize to avoid runaway memory usage.
task_queue: Queue = Queue(maxsize=1000)


def insert_task_to_queue(job_id: str, job_data: Dict[str, Any]) -> bool:
    """
    Safely enqueue a new task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing all data required to execute the task.

    Returns
    -------
    bool
        ``True`` if the task was successfully added to the queue,
        ``False`` otherwise (e.g., when the queue is full).

    Notes
    -----
    - The function does **not** raise exceptions; instead it logs the
      failure and returns ``False``.
    - The queue's `maxsize` prevents unbounded growth, mitigating
      CWE‑770.
    """
    # Basic validation to avoid inserting malformed entries
    if not isinstance(job_id, str) or not job_id:
        _logger.warning("Attempted to insert task with invalid job_id: %r", job_id)
        return False

    if not isinstance(job_data, dict):
        _logger.warning("job_data must be a dict; got %r", type(job_data))
        return False

    task_payload = {"job_id": job_id, "job_data": job_data}

    try:
        # `block=False` ensures we don't block the calling thread
        task_queue.put(task_payload, block=False)
    except Full:
        _logger.error(
            "Task queue is full (maxsize=%d). Unable to enqueue job_id=%s",
            task_queue.maxsize,
            job_id,
        )
        return False
    except Exception as exc:  # pragma: no cover
        _logger.exception("Unexpected error when enqueuing job_id=%s: %s", job_id, exc)
        return False

    _logger.debug("Enqueued job_id=%s successfully.", job_id)
    return True