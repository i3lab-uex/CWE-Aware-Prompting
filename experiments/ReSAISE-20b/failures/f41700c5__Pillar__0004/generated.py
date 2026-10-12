import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread‑safe access
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user information in the global `user_cache`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        A dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the caching succeeded, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(identifier, str) or not identifier:
        return False

    if not isinstance(data_info, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental mutation of the original dict
            user_cache[identifier] = data_info.copy()
        return True
    except Exception:
        # In a real application you might log the exception here.
        return False