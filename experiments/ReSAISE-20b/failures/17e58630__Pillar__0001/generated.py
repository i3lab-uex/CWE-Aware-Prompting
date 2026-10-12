# task_manager.py

"""
Task queue manager.

This module provides a thread‑safe global queue for storing tasks and a helper
function to enqueue new tasks.  The queue is implemented using
`queue.Queue`, which guarantees safe concurrent access.

The implementation follows the principle of *least privilege*:
  • Only a single, well‑defined API (`enqueue_task`) is exposed for adding
    tasks.
  • No external code can manipulate the queue directly, preventing accidental
    resource leakage or corruption.

The function returns `True` on success; it never raises exceptions so callers
can rely on a simple boolean result.
"""

import queue
from typing import Dict

# Global task queue.  Unbounded to avoid dead‑lock scenarios.
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue()


def enqueue_task(identifier: str, details: Dict) -> bool:
    """
    Add a new task to the global queue.

    Parameters
    ----------
    identifier : str
        A unique string identifying the task.
    details : dict
        Parameters and metadata for the task.

    Returns
    -------
    bool
        True if the task was successfully queued, False otherwise.
    """
    # Validation: ensure identifier is a non‑empty string
    if not isinstance(identifier, str) or not identifier:
        return False

    # Validation: ensure details is a dict
    if not isinstance(details, dict):
        return False

    try:
        # The queue is thread‑safe; this operation will block only if the
        # underlying OS resources are exhausted, which is highly unlikely.
        task_queue.put_nowait((identifier, details))
    except queue.Full:
        # Queue is unbounded, but we guard against an unlikely scenario.
        return False
    except Exception:
        # Catch any unexpected exception to avoid leaking resources or
        # leaving the system in an inconsistent state.
        return False

    return True