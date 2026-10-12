import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Cache user data in memory.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user. Must be a non-empty string.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(user_id, str) or not user_id:
        return False

    if not isinstance(user_data, dict):
        return False

    # Store a shallow copy to avoid external mutation affecting the cache
    try:
        with _user_cache_lock:
            user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # In a real application we might log this exception
        return False