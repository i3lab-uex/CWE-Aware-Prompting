#!/usr/bin/env python3
"""
In‑memory cache for user data with a simple size limit to mitigate CWE‑770.

The module defines:
    - `user_cache`: a global dictionary storing cached data.
    - `cache_client_data(client_id, client_data)`: stores the given data in the cache.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# Maximum number of cached entries to prevent unbounded memory growth.
_MAX_CACHE_SIZE: int = 1_000

# Global cache instance (thread‑safe).
_user_cache_lock = threading.RLock()
_user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()


def _evict_if_needed() -> None:
    """Evict the oldest entry if cache size exceeds the maximum."""
    while len(_user_cache) > _MAX_CACHE_SIZE:
        # popitem(last=False) removes the first item inserted (FIFO order).
        _user_cache.popitem(last=False)


def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store user data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(client_id, str):
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Insert or update the entry. The OrderedDict preserves insertion order.
            _user_cache[client_id] = client_data
            # Move the key to the end to mark it as most recently used.
            _user_cache.move_to_end(client_id)
            _evict_if_needed()
        return True
    except Exception:
        # Log the exception in a real application.
        return False


# Expose the cache for testing or inspection (read‑only).
def get_cached_client_data(client_id: str) -> Dict[str, Any] | None:
    """Retrieve cached data for a given client_id."""
    with _user_cache_lock:
        return _user_cache.get(client_id)


# Example usage (remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    assert cache_client_data("user123", {"name": "Alice", "age": 30})
    assert get_cached_client_data("user123") == {"name": "Alice", "age": 30}
    print("Cache test passed.")