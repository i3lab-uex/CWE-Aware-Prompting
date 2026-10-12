import queue
from typing import Dict

# Global task queue used by the application.
# `maxsize=0` means the queue size is infinite.
task_queue: "queue.Queue[tuple[str, Dict]]" = queue.Queue(maxsize=0)


def push_task(uid: str, data: Dict) -> bool:
    """
    Push a new task into the global task queue.

    Parameters
    ----------
    uid : str
        A unique identifier for the task.
    data : dict
        Task-specific parameters and information.

    Returns
    -------
    bool
        ``True`` if the task was successfully enqueued, otherwise ``False``.

    Notes
    -----
    * The function is thread‑safe thanks to :class:`queue.Queue`.
    * No exception is propagated – any internal error results in a ``False`` return.
    """
    try:
        # Queue.put is thread‑safe and will block if the queue is full.
        task_queue.put((uid, data), block=False)
        return True
    except queue.Full:
        # Queue is full; task cannot be added.
        return False
    except Exception:
        # Catch any unexpected error to avoid leaking internal state.
        return False