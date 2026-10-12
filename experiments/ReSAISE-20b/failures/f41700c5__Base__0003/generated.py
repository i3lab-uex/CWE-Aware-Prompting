#!/usr/bin/env python3
"""
A lightweight, thread‑safe in‑memory cache for user data.

This module defines a single function `store_user_info` that stores
user‑specific information in a global dictionary.  To mitigate
CWE‑770 (unbounded resource allocation) the cache is bounded to a
maximum size (`MAX_CACHE_SIZE`).  When the limit is reached, the least
recently used entry is evicted before inserting a new one.
"""

import threading
from collections import OrderedDict

# Global cache and associated lock for thread safety
user_cache: dict[str, dict] = OrderedDict()
CACHE_LOCK = threading.Lock()

# Maximum number of entries the cache may hold
MAX_CACHE_SIZE: int = 10_000


def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    identifier : str
        Unique identifier for the user.
    data_info : dict
        Dictionary containing arbitrary user‑related information.

    Returns
    -------
    bool
        ``True`` if the data was stored successfully, otherwise ``False``.

    Notes
    -----
    * The cache is bounded by :data:`MAX_CACHE_SIZE`.  When the limit
      is reached, the least recently used (LRU) entry is removed.
    * Thread safety is guaranteed by :data:`CACHE_LOCK`.
    """
    if not isinstance(identifier, str):
        return False
    if not isinstance(data_info, dict):
        return False

    with CACHE_LOCK:
        # Evict LRU entry if we exceed the maximum size
        if identifier not in user_cache and len(user_cache) >= MAX_CACHE_SIZE:
            # popitem(last=False) pops the first (LRU) item
            user_cache.popitem(last=False)

        # Store or update the entry and mark it as most recently used
        user_cache[identifier] = data_info
        # Move to the end to indicate recent use
        user_cache.move_to_end(identifier)

    return True