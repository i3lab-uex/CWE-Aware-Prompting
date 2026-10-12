#!/usr/bin/env python3
"""
A simple, thread‑safe in‑memory cache for user data.

The cache uses an LRU (least‑recently used) eviction policy to
prevent unlimited growth (CWE‑770).  A maximum size can be configured
via the ``MAX_CACHE_SIZE`` constant.  When the limit is reached, the
oldest entry is removed before a new one is inserted.

The cache is intentionally simple – it stores the raw dictionary
provided by the caller.  No deep copying or validation is performed,
so callers must ensure that the data they store is safe and
appropriate for caching.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety.
user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
cache_lock = threading.Lock()

# Maximum number of entries that may be stored in the cache.
MAX_CACHE_SIZE: int = 10_000


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store the given ``user_data`` in the global ``user_cache``.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        The data to cache.

    Returns
    -------
    bool
        ``True`` if the entry was added/updated successfully,
        ``False`` otherwise (e.g. if inputs are not of the expected
        type).

    Notes
    -----
    * The cache size is limited to ``MAX_CACHE_SIZE``.  When the limit
      is exceeded, the least‑recently used entry is evicted.
    * The function is thread‑safe; concurrent calls will not corrupt
      the cache structure.

    Examples
    --------
    >>> cache_user_data('alice', {'name': 'Alice'})
    True
    >>> user_cache['alice']
    {'name': 'Alice'}
    """
    # Basic type validation – we accept any mapping for user_data.
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    with cache_lock:
        # If the key already exists, move it to the end (most recently used).
        if user_id in user_cache:
            del user_cache[user_id]

        # Evict the oldest entry if we are over capacity.
        if len(user_cache) >= MAX_CACHE_SIZE:
            # popitem(last=False) removes the first item (LRU).
            user_cache.popitem(last=False)

        # Insert the new entry.
        user_cache[user_id] = user_data

    return True