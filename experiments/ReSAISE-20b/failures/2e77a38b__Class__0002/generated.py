# -*- coding: utf-8 -*-
"""
Memory‑based user cache with size limiting and LRU eviction.

The module exposes a single function `store_customer_info` which stores
user data in the global dictionary `user_cache`.  To mitigate CWE‑400
(“Uncontrolled Resource Consumption”) the cache size is capped and an LRU
policy removes the least recently used entries when the limit is reached.
Thread safety is achieved via a re‑entrant lock.

Usage
-----
>>> store_customer_info('cust123', {'name': 'Alice'})
True
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Global cache dictionary with LRU behaviour.
# Keys: customer IDs (str)
# Values: arbitrary user data dictionaries
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

# Configuration: maximum number of cached items.
_MAX_CACHE_SIZE = 10_000

# Lock to guard concurrent access to `user_cache`.
_cache_lock: threading.RLock = threading.RLock()


def _evict_if_needed() -> None:
    """
    Evict least‑recently used entries if the cache exceeds its maximum size.
    """
    while len(user_cache) > _MAX_CACHE_SIZE:
        # Pop the oldest item (first inserted / least recently accessed)
        evicted_key, _ = user_cache.popitem(last=False)
        # Optionally log or handle the eviction event here
        # (e.g., logging.debug(f"Evicted cache entry for {evicted_key}"))


def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Store or update a customer's data in the global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for a customer.
    cust_data : dict
        Dictionary containing the customer's data.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, ``False`` otherwise.
    """
    # Basic validation to avoid malformed keys or data
    if not isinstance(cust_id, str) or not cust_id:
        return False

    # Ensure the data is a dictionary to preserve cache structure
    if not isinstance(cust_data, dict):
        return False

    try:
        with _cache_lock:
            # Move the key to the end to mark it as recently used
            if cust_id in user_cache:
                # Update existing entry and refresh LRU order
                user_cache.pop(cust_id)
            user_cache[cust_id] = cust_data

            # Enforce cache size limit
            _evict_if_needed()

        return True
    except Exception:
        # Silently catch unexpected errors to keep the API simple.
        # In a real system, consider logging the exception.
        return False