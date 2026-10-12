# -*- coding: utf-8 -*-
"""
In‑memory caching for user profile data with size throttling to mitigate
CWE‑770 (unbounded resource allocation).

The module exposes a single function `cache_profile_data` that stores
profile information in a global cache.  When the maximum number of cached
entries is reached, the oldest entry is removed (simple LRU policy).
"""

from __future__ import annotations

import collections
import threading
from typing import Dict, Any

# Global cache (thread‑safe via a lock)
_user_cache: collections.OrderedDict[str, Dict[str, Any]] = collections.OrderedDict()
_cache_lock = threading.RLock()

# Maximum number of cached profiles to prevent unbounded growth.
_MAX_CACHE_SIZE: int = 1_000


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user profile in the global cache.

    Parameters
    ----------
    profile_id : str
        A unique identifier for the user.
    profile_data : dict
        Dictionary containing arbitrary user data.

    Returns
    -------
    bool
        True if the profile was cached successfully, False otherwise.
    """
    try:
        with _cache_lock:
            # If the profile already exists, move it to the end (most recently used)
            if profile_id in _user_cache:
                _user_cache.move_to_end(profile_id)

            # Insert/overwrite the profile
            _user_cache[profile_id] = dict(profile_data)  # shallow copy to avoid accidental mutation

            # Enforce cache size limit
            if len(_user_cache) > _MAX_CACHE_SIZE:
                # Remove the oldest entry (first item)
                _user_cache.popitem(last=False)

        return True
    except Exception:
        # Swallow all exceptions to satisfy the "Raise: None" contract.
        return False


# Optional helper for retrieving cached data (not part of the required API)
def get_cached_profile(profile_id: str) -> Dict[str, Any] | None:
    """
    Retrieve a cached profile if present.

    Parameters
    ----------
    profile_id : str

    Returns
    -------
    dict or None
        The cached profile data, or None if not found.
    """
    with _cache_lock:
        return _user_cache.get(profile_id)