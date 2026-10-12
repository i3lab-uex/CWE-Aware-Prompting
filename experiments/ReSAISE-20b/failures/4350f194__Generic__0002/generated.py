import threading
from typing import Dict

# Global cache dictionary and a lock for thread‑safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Store user data in the global `user_cache` dictionary.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user. Must be a non‑empty string.
    user_data : dict
        A dictionary containing user information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    try:
        # Use a copy to prevent external mutation of cached data
        with _user_cache_lock:
            user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # Any unexpected error (e.g., memory issues) results in failure
        return False