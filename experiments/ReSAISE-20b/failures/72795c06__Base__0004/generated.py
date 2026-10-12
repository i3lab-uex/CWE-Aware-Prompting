# -*- coding: utf-8 -*-
"""
In‑memory caching of user profile data with a simple LRU eviction policy.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Global cache dictionary with a maximum size to mitigate CWE‑770
_MAX_CACHE_SIZE = 10_000   # configurable upper bound

# Using an OrderedDict to maintain insertion order for LRU eviction
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

# Lock to make cache operations thread‑safe
_cache_lock = threading.RLock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Cache the given user profile data.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    if not isinstance(profile_id, str) or not profile_id:
        return False

    # Defensive copy to prevent accidental mutation of cached data
    try:
        data_copy = dict(profile_data)
    except Exception:  # pragma: no cover
        return False

    with _cache_lock:
        # If the key already exists, move it to the end (most recently used)
        if profile_id in user_cache:
            user_cache.move_to_end(profile_id)

        # Insert or update the cache entry
        user_cache[profile_id] = data_copy

        # Enforce maximum cache size using LRU eviction
        if len(user_cache) > _MAX_CACHE_SIZE:
            # popitem(last=False) removes the oldest item
            user_cache.popitem(last=False)

    return True