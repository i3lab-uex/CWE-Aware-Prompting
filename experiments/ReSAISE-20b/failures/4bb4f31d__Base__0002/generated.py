# -*- coding: utf-8 -*-
"""
Memory‑based caching system for user data.

This module provides a simple in‑memory cache that stores user information
identified by a unique client_id.  To mitigate CWE‑770 (unbounded resource
allocation) the cache is bounded by a configurable maximum size.  When the
limit is reached, the least recently used entry is evicted.

Author: OpenAI ChatGPT
"""

from collections import OrderedDict
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Maximum number of user entries the cache can hold.
# Adjust this value according to available memory and expected usage patterns.
MAX_CACHE_SIZE: int = 10_000

# --------------------------------------------------------------------------- #
# Global cache instance
# --------------------------------------------------------------------------- #

# OrderedDict preserves insertion order, enabling simple LRU eviction.
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    info_data : dict
        Dictionary containing arbitrary user information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (e.g., invalid input).

    Notes
    -----
    - The cache is bounded by :data:`MAX_CACHE_SIZE`.  When the limit is
      reached, the least recently used entry is evicted.
    - No explicit error handling is performed; invalid input simply
      results in ``False`` being returned.
    """
    # Basic validation: ensure client_id is a non‑empty string
    if not isinstance(client_id, str) or not client_id:
        return False

    # Ensure info_data is a dictionary
    if not isinstance(info_data, dict):
        return False

    # Insert or update the entry
    if client_id in user_cache:
        # Move to end to mark as recently used
        user_cache.move_to_end(client_id)
    else:
        # Evict if we are at capacity
        if len(user_cache) >= MAX_CACHE_SIZE:
            # Pop the oldest item (LRU)
            user_cache.popitem(last=False)

    # Store a shallow copy to avoid accidental external mutation
    user_cache[client_id] = dict(info_data)
    return True


# --------------------------------------------------------------------------- #
# Example usage (comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Basic test
    assert cache_application_data("user123", {"name": "Alice", "age": 30})
    assert user_cache["user123"]["name"] == "Alice"
    print("Cache test passed.")