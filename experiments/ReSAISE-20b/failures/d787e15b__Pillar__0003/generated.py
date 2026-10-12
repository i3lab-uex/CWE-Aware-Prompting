import threading
from queue import Queue, Full

# Global task queue with a reasonable maxsize to prevent uncontrolled growth.
# Adjust `maxsize` as needed for your environment. A value of 0 means infinite size.
task_queue: Queue = Queue(maxsize=0)

# A lock to guard against race conditions when checking for duplicates.
# This is optional but helps maintain consistent state in multi‑threaded contexts.
_task_lock = threading.Lock()
# A set to keep track of registered task references for quick duplicate detection.
_registered_task_refs = set()


def register_new_task(task_reference: str, parameters: dict) -> bool:
    """
    Register a new task in the global queue.

    Parameters
    ----------
    task_reference : str
        A unique string that identifies the task.
    parameters : dict
        Dictionary containing details and parameters for the task.

    Returns
    -------
    bool
        True if the task was added successfully, False otherwise.
    """
    # Basic validation: ensure the reference is a non‑empty string and parameters are a dict.
    if not isinstance(task_reference, str) or not task_reference:
        return False
    if not isinstance(parameters, dict):
        return False

    # Prevent duplicate registrations.
    with _task_lock:
        if task_reference in _registered_task_refs:
            # Duplicate detected; do not enqueue again.
            return False
        _registered_task_refs.add(task_reference)

    # Construct the task payload. The structure can be adjusted to suit your consumer.
    task_payload = {
        "reference": task_reference,
        "parameters": parameters
    }

    try:
        # Attempt to enqueue the task. If the queue is full, this will raise Full.
        task_queue.put_nowait(task_payload)
    except Full:
        # Queue full; remove the reference from the set to allow future attempts.
        with _task_lock:
            _registered_task_refs.discard(task_reference)
        return False
    except Exception:
        # Any unexpected exception should also clean up the reference set.
        with _task_lock:
            _registered_task_refs.discard(task_reference)
        return False

    return True