#!/usr/bin/env python3
"""
Module: task_queue_manager

Provides a simple interface for adding tasks to a globally shared queue.
"""

from __future__ import annotations

import queue
from typing import Dict, Tuple


# Global task queue (unbounded by default; can be configured with a maxsize if needed)
task_queue: queue.Queue[Tuple[str, Dict]] = queue.Queue()


def insert_task_to_queue(job_id: str, job_data: Dict) -> bool:
    """
    Insert a task into the global `task_queue`.

    Parameters
    ----------
    job_id : str
        A unique identifier for the task.
    job_data : dict
        Dictionary containing task details, parameters, etc.

    Returns
    -------
    bool
        True if the task was successfully added; False otherwise.
    """
    # Basic validation to guard against misuse
    if not isinstance(job_id, str) or not job_id:
        return False
    if not isinstance(job_data, dict):
        return False

    try:
        # Use a non-blocking put to avoid hanging if the queue is full
        task_queue.put_nowait((job_id, job_data))
    except queue.Full:
        # Queue reached its maxsize (if one was set)
        return False
    except Exception:
        # Any unexpected exception is swallowed and reported as failure
        return False

    return True