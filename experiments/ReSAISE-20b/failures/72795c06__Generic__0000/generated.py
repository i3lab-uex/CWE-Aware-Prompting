# In-memory cache for user profiles

from typing import Dict, Any
import threading

# Global dictionary acting as the cache store
user_cache: Dict[str, Dict[str, Any]] = {}
# A lock to ensure thread‑safe access to the cache
_cache_lock = threading.RLock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user's profile data in the global `user_cache`.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(profile_id, str) or not profile_id:
        return False

    if not isinstance(profile_data, dict):
        return False

    try:
        with _cache_lock:
            # Perform a shallow copy to prevent accidental external mutation
            user_cache[profile_id] = profile_data.copy()
        return True
    except Exception:
        # In a real application you might log the exception here.
        return False