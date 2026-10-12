#!/usr/bin/env python3
"""
In‑memory user data cache.

The module exposes a single function `cache_client_data` that stores
user‑specific information in a global cache.  The implementation uses an
``OrderedDict`` to maintain insertion order so that the oldest entry can be
evicted when a maximum cache size is reached, mitigating CWE‑400
(“Uncontrolled Resource Consumption”).

The cache and its configuration are thread‑safe via a global lock.
"""

from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration & global objects
# --------------------------------------------------------------------------- #

#: Maximum number of entries allowed in the cache.  `None` means unlimited.
MAX_CACHE_SIZE: int | None = 10_000

#: Global cache dictionary. Keys are `client_id`s, values are the user data.
user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()

#: Global lock for thread‑safety.
_cache_lock = threading.RLock()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store `client_data` in the global cache under the key `client_id`.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    client_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        ``True`` if the data was stored successfully, ``False`` otherwise.

    Notes
    -----
    * The function validates that `client_id` is a non‑empty string and
      `client_data` is a dictionary.  Invalid arguments result in ``False``.
    * When the cache exceeds :data:`MAX_CACHE_SIZE`, the oldest entry
      (the one that was inserted first) is evicted to keep the cache size
      bounded.
    * Thread‑safety is guaranteed by :data:`_cache_lock`.
    """
    # Basic argument validation
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(client_data, dict):
        return False

    with _cache_lock:
        # Insert or update the entry
        user_cache[client_id] = client_data

        # Move to end to mark as most recently used
        user_cache.move_to_end(client_id)

        # Enforce cache size limit if configured
        if MAX_CACHE_SIZE is not None and len(user_cache) > MAX_CACHE_SIZE:
            # Pop the oldest item (first inserted)
            user_cache.popitem(last=False)

    return True


# --------------------------------------------------------------------------- #
# Optional helper: retrieve cached data
# --------------------------------------------------------------------------- #

def get_cached_client_data(client_id: str) -> Dict[str, Any] | None:
    """
    Retrieve cached data for a given `client_id`, if present.

    Parameters
    ----------
    client_id : str
        The user identifier to look up.

    Returns
    -------
    dict | None
        The cached data or ``None`` if not found.
    """
    with _cache_lock:
        return user_cache.get(client_id)


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate cache
    for i in range(12):
        cid = f"user_{i}"
        data = {"name": f"User {i}", "role": "member"}
        success = cache_client_data(cid, data)
        print(f"Cached {cid}: {'OK' if success else 'FAIL'}")

    # Display cache contents
    print("\nCurrent cache entries:")
    for key, value in user_cache.items():
        print(f"{key}: {value}")