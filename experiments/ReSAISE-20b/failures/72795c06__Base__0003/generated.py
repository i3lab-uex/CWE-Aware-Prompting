#!/usr/bin/env python3
"""
In‑memory user profile cache.

The cache is a simple dictionary keyed by `profile_id`.  To mitigate
CWE‑770 (unbounded resource allocation) a hard limit on the number of
entries is enforced.  When the cache size would exceed this limit, the
caching operation fails and returns ``False``; no exception is raised.

Thread safety is provided by a re‑entrant lock so that concurrent
accesses from multiple threads do not corrupt the internal state.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its associated lock.
user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.RLock()

# Maximum number of entries allowed in the cache.
MAX_CACHE_SIZE: int = 10_000


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user's profile data in the global ``user_cache``.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing arbitrary profile information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``
        (e.g., when the cache size limit would be exceeded).
    """
    if not isinstance(profile_id, str):
        return False
    if not isinstance(profile_data, dict):
        return False

    with _cache_lock:
        # If the entry already exists, replace it without affecting size.
        if profile_id in user_cache:
            user_cache[profile_id] = profile_data
            return True

        # Enforce the maximum cache size.
        if len(user_cache) >= MAX_CACHE_SIZE:
            return False

        user_cache[profile_id] = profile_data
        return True


# Optional: expose a helper to clear the cache (useful for tests or resets).
def clear_user_cache() -> None:
    """Clear all entries from the global user cache."""
    with _cache_lock:
        user_cache.clear()