import threading
from typing import Dict

# Global cache dictionary and lock for thread safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Store user data in an in-memory cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type validation to avoid corrupting the cache
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    # Avoid storing empty data unless explicitly intended
    if not user_data:
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to prevent accidental external modifications
            user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # In a real application, log the exception here.
        return False