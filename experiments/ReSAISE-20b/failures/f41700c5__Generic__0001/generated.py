# memory_cache.py

"""
A simple, thread‑safe in‑memory cache for user data.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global `user_cache`.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        A dictionary containing various user‑related information.

    Returns
    -------
    bool
        True if the data was stored successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(identifier, str) or not identifier:
        return False

    if not isinstance(data_info, dict):
        return False

    # Avoid storing empty data
    if not data_info:
        return False

    try:
        with _user_cache_lock:
            # Create a shallow copy to prevent external mutation.
            user_cache[identifier] = data_info.copy()
        return True
    except Exception:
        # In a real application you might log the exception.
        return False