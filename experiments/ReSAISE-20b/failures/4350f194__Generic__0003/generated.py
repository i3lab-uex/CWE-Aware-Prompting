# user_cache.py

from __future__ import annotations
import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread‑safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store user data in the global cache.

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
    # Basic validation: ensure user_id is a non‑empty string and
    # user_data is a dictionary.
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to prevent accidental mutation
            user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # In a real application you might log the exception.
        return False