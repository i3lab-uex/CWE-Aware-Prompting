# -*- coding: utf-8 -*-
"""
Memory based cache for user data.

This module implements a simple, thread‑safe LRU cache that holds
user specific information in memory.  It protects against unbounded
memory growth (CWE‑770) by limiting the total number of cached items.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Maximum number of items to keep in the cache.
_MAX_CACHE_SIZE = 10_000

# Global cache: maps client_id -> info_data
user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
# Lock to serialize access to the cache
_cache_lock = threading.Lock()


def _evict_if_needed() -> None:
    """
    Evicts the least recently used item when the cache exceeds
    :data:`_MAX_CACHE_SIZE`.  Called while holding :data:`_cache_lock`.
    """
    if len(user_cache) > _MAX_CACHE_SIZE:
        # popitem(last=False) removes the first item inserted (LRU)
        user_cache.popitem(last=False)


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user specific information in the global cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    info_data : dict
        Dictionary containing any user related data.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, ``False`` otherwise.
    """
    # Basic type validation – we avoid raising exceptions as per spec
    if not isinstance(client_id, str) or not isinstance(info_data, dict):
        return False

    try:
        with _cache_lock:
            # Insert or update the entry
            user_cache[client_id] = info_data
            # Move to end to mark as most recently used
            user_cache.move_to_end(client_id, last=True)
            _evict_if_needed()
        return True
    except Exception:
        # In a real application you might log the exception here.
        return False