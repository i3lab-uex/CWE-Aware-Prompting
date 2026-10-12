# cache_user_data.py

"""
User data caching module.

This module provides a simple in‑memory cache for user data.  It
implements a maximum size limit to avoid unbounded memory growth
(CWE‑770).  When the cache is full, new entries are rejected and the
function returns False.  The module is thread‑safe using a lock.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and a lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries the cache may hold
_MAX_CACHE_SIZE: int = 10_000


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Cache user data in memory.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the data was cached successfully, False if the cache is full.
    """
    # Basic validation
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    with _user_cache_lock:
        # Reject new entries when the cache is full
        if len(user_cache) >= _MAX_CACHE_SIZE:
            return False

        # Store the data
        user_cache[user_id] = user_data.copy()  # shallow copy to avoid accidental mutation

    return True