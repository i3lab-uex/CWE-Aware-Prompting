import threading
from typing import Dict

# Global in-memory cache for user profiles.
user_cache: Dict[str, dict] = {}
# Lock to make cache access thread‑safe.
_cache_lock = threading.Lock()


def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store user profile data in the global `user_cache`.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing the user's profile information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid accidental misuse
    if not isinstance(profile_id, str) or not isinstance(profile_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to prevent accidental mutation of the original dict
            user_cache[profile_id] = profile_data.copy()
        return True
    except Exception:
        # No exceptions should be raised; return False on failure.
        return False