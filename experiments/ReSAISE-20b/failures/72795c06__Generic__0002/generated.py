# In-memory caching of user profile data

from typing import Dict, Any
import threading

# Global cache dictionary and lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store user profile data in the global cache.

    Args:
        profile_id (str): Unique identifier for a user.
        profile_data (dict): Dictionary containing user details.

    Returns:
        bool: True if caching succeeded, False otherwise.
    """
    try:
        # Basic type validation (non-str keys in profile_data are allowed)
        if not isinstance(profile_id, str):
            return False
        if not isinstance(profile_data, dict):
            return False

        # Store data atomically with a lock
        with _user_cache_lock:
            user_cache[profile_id] = profile_data.copy()

        return True
    except Exception:
        # Log exception in real application; here we simply return False
        return False