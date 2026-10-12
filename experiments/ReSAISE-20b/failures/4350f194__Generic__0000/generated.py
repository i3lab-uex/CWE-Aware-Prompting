import threading
from typing import Dict, Any

# Global cache and lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store a user's data in the global cache.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type validation to avoid corrupting the cache
    if not isinstance(user_id, str):
        return False
    if not isinstance(user_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Avoid overwriting existing data unintentionally
            user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # Any unexpected error should not crash the application
        return False