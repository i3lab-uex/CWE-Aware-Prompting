import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread‑safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store user-specific data in an in-memory cache.

    Parameters
    ----------
    profile_id : str
        A unique identifier for the user.
    profile_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation to avoid corrupting the cache
    if not isinstance(profile_id, str) or not profile_id:
        return False
    if not isinstance(profile_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Use a shallow copy to prevent external mutation
            user_cache[profile_id] = dict(profile_data)
        return True
    except Exception:
        # In a real system we would log the exception; here we simply return False
        return False