# -*- coding: utf-8 -*-
"""
A simple in‑memory user data cache.

The implementation protects against uncontrolled resource consumption
(CWE‑400) by limiting the maximum number of cached entries.  When the
limit is reached, new items are rejected instead of silently expanding
the dictionary indefinitely.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache and configuration -------------------------------------------------

MAX_CACHE_SIZE: int = 10_000  # maximum number of users to cache
_user_cache_lock = threading.RLock()
user_cache: Dict[str, Dict[str, Any]] = {}

# -------------------------------------------------------------------------------

def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store a user's data in the global cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(user_id, str) or not user_id:
        return False
    if not isinstance(user_data, dict):
        return False

    with _user_cache_lock:
        # If the cache is full, refuse to add new entries
        if len(user_cache) >= MAX_CACHE_SIZE and user_id not in user_cache:
            return False

        # Store or update the entry
        user_cache[user_id] = user_data.copy()  # copy to avoid external mutation

    return True