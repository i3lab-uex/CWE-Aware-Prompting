# -*- coding: utf-8 -*-

"""
Utility for inserting tasks into a shared queue in a parallel processing system.
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# Global queue used by the system. It should be instantiated elsewhere in the application.
# Here we provide a default placeholder for type checking; the actual queue must be
# assigned before calling `insert_task_to_queue`.
task_queue: "Queue[tuple[str, Dict[str, Any]]]" = None  # type: ignore

def insert_task_to_queue(job_id: str, job_data: Dict[str, Any]) -> bool:
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
        ``True`` if the task was successfully added, otherwise ``False``.

    Notes
    -----
    * The function assumes that `task_queue` is a thread‑safe queue instance
      (e.g., :class:`queue.Queue`). It does **not** create the queue.
    * Any exception raised by the underlying queue implementation is caught
      and logged; the function then returns ``False``.
    """
    global task_queue

    if task_queue is None:
        logging.error("Global task queue has not been initialized.")
        return False

    try:
        # The queue expects a tuple of (job_id, job_data).  If the
        # application uses a different structure, adapt this accordingly.
        task_queue.put((job_id, job_data), block=False)
    except Exception as exc:
        logging.exception("Failed to insert task %s into queue: %s", job_id, exc)
        return False

    return True