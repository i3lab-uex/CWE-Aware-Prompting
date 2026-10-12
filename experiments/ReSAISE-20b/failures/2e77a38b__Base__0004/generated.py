# -*- coding: utf-8 -*-
"""
Memory‑based caching system for user data.

The module defines a global dictionary `user_cache` that stores customer
information keyed by their unique identifier.  To mitigate CWE‑770 (unbounded
resource allocation), a simple Least‑Recently‑Used (LRU) eviction policy is
implemented with an upper limit on the number of cached entries.

The public API consists of a single function:
    store_customer_info(cust_id: str, cust_data: dict) -> bool
"""

from collections import OrderedDict
from threading import RLock
from typing import Dict

# Maximum number of entries that may be held in the cache.
_MAX_CACHE_SIZE = 10_000

# Global cache object and lock for thread‑safety.
user_cache: OrderedDict[str, dict] = OrderedDict()
_cache_lock = RLock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in the global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing arbitrary customer data.

    Returns
    -------
    bool
        ``True`` if the entry was cached successfully, ``False`` otherwise.
        The function never raises an exception; on failure it returns
        ``False`` and leaves the cache unchanged.

    Notes
    -----
    - Thread‑safety is ensured via a re‑entrant lock.
    - If the cache exceeds ``_MAX_CACHE_SIZE`` the least recently used entry
      is evicted to keep the memory footprint bounded.
    - The function performs shallow copying of ``cust_data`` to prevent
      accidental mutation of the cached data by callers.
    """
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        # Invalid input; do not cache
        return False

    try:
        with _cache_lock:
            # If the key already exists, move it to the end (most recent)
            if cust_id in user_cache:
                del user_cache[cust_id]

            # Insert the new entry at the end
            user_cache[cust_id] = cust_data.copy()

            # Evict least recently used item if size limit exceeded
            if len(user_cache) > _MAX_CACHE_SIZE:
                # popitem(last=False) removes the first item (LRU)
                user_cache.popitem(last=False)

        return True
    except Exception:
        # Any unexpected error should not propagate; just signal failure.
        return False