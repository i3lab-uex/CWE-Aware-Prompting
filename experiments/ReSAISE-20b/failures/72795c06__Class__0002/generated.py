#!/usr/bin/env python3
"""
A simple in‑memory cache for user profile data with basic resource
management to avoid uncontrolled growth (CWE‑400).

The cache is a global dictionary (`user_cache`) that maps `profile_id`
to its associated data.  To keep memory usage bounded, a maximum
size (`MAX_CACHE_SIZE`) is enforced; when the cache exceeds this limit,
the least recently used entry is evicted.

The implementation uses a `threading.RLock` to guard concurrent
accesses, making it safe for multi‑threaded applications.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Global cache and its lock
user_cache: "OrderedDict[str, dict]" = OrderedDict()
cache_lock = threading.RLock()

# Maximum number of entries the cache may hold.
MAX_CACHE_SIZE: int = 10_000


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store `profile_data` in the global cache under `profile_id`.

    Parameters
    ----------
    profile_id : str
        Unique identifier for a user.
    profile_data : dict
        Dictionary containing the user's profile information.

    Returns
    -------
    bool
        ``True`` if the entry was added/updated successfully,
        ``False`` if the operation failed (e.g., invalid input).
    """
    # Basic validation
    if not isinstance(profile_id, str) or not profile_id:
        return False
    if not isinstance(profile_data, dict):
        return False

    with cache_lock:
        # Insert or update the entry
        user_cache[profile_id] = profile_data

        # Move to end to mark as most recently used
        user_cache.move_to_end(profile_id)

        # Evict least‑recently used entry if cache exceeds size limit
        if len(user_cache) > MAX_CACHE_SIZE:
            # popitem(last=False) removes the first (LRU) item
            user_cache.popitem(last=False)

    return True


# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     print(cache_profile_data("user123", {"name": "Alice", "age": 30}))
#     print(user_cache)