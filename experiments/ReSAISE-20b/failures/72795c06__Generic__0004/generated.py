# Simple in‑memory cache for user profiles

from __future__ import annotations
import threading
from typing import Dict, Any

# Global cache dictionary and lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user's profile data in the global cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        ``True`` if the data was stored successfully, otherwise ``False``.

    Notes
    -----
    - The function uses a re‑entrant lock to guard the global cache,
      ensuring thread safety in multi‑threaded environments.
    - A shallow copy of ``profile_data`` is stored to avoid accidental
      mutation of the original dictionary by callers.
    """
    if not isinstance(profile_id, str):
        return False
    if not isinstance(profile_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to prevent external modifications
            user_cache[profile_id] = profile_data.copy()
        return True
    except Exception:
        # Log the exception in a real application; here we simply swallow it.
        return False