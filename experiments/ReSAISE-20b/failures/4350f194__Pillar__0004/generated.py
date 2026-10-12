import threading
from typing import Dict

# Global cache dictionary and a lock for thread safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Cache user data in the global `user_cache` dictionary.

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
    # Basic validation to avoid storing malformed data
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Overwrite any existing entry for this user_id
            user_cache[user_id] = dict(user_data)  # shallow copy to avoid accidental mutation
        return True
    except Exception:
        # In a real application, log the exception here.
        return False