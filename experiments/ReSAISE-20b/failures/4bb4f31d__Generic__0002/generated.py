import threading
from typing import Dict

# Global cache dictionary and a lock for thread‑safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Stores user‑specific information in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    info_data : dict
        Dictionary containing user‑related data to cache.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    - The function is thread‑safe.
    - It performs basic type checking and sanitises the data
      to prevent accidental modification of cached objects.
    - If ``info_data`` is not a dictionary, the function fails gracefully
      and returns ``False``.
    """
    # Basic type validation
    if not isinstance(client_id, str) or not isinstance(info_data, dict):
        return False

    try:
        # Use a copy to avoid accidental external mutation
        data_copy = dict(info_data)

        with _user_cache_lock:
            user_cache[client_id] = data_copy
    except Exception:
        # Any exception (e.g., memory error) results in failure
        return False

    return True