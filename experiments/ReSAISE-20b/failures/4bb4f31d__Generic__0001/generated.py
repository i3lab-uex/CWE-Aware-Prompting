# -*- coding: utf-8 -*-
"""
Memory‑based caching system for user data.
"""

import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    info_data : dict
        Dictionary containing user-related data to be cached.

    Returns
    -------
    bool
        True if the caching operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    # Prevent storing None or empty dictionaries unless explicitly intended
    if info_data is None:
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to avoid accidental external modifications
            user_cache[client_id] = dict(info_data)
        return True
    except Exception:
        # In a real-world scenario, log the exception here.
        return False