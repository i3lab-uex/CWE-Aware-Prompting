#!/usr/bin/env python3
"""
A simple in‑memory cache for client information.

The module keeps a global dictionary `user_cache` that maps a unique
client identifier to the client's data dictionary.  Two limits are
enforced:

* `MAX_CACHE_SIZE` – maximum total size in bytes of all cached values.
* `MAX_CLIENTS`    – maximum number of entries that may be stored.

If either limit would be exceeded by adding a new entry, the function
returns ``False`` and does not modify the cache.

Thread safety is provided by a re‑entrant lock.  The implementation
uses ``sys.getsizeof`` to estimate the memory footprint of each entry.
"""

from __future__ import annotations

import sys
import threading
from typing import Dict, Any

# Global cache and its associated lock
user_cache: Dict[str, Dict[str, Any]] = {}
cache_lock = threading.RLock()

# Configuration limits
MAX_CACHE_SIZE: int = 10 * 1024 * 1024      # 10 MiB
MAX_CLIENTS: int = 5000                     # arbitrary client count limit


def _current_cache_size() -> int:
    """
    Estimate the total memory usage of all cached values.
    Note: ``sys.getsizeof`` is only an approximation and does not
    account for shared objects.
    """
    return sum(sys.getsizeof(v) for v in user_cache.values())


def cache_client_info(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store the client's data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the client.
    client_data : dict
        Dictionary containing the client's information.

    Returns
    -------
    bool
        ``True`` if the entry was added/updated successfully.
        ``False`` if adding would violate size or count limits.

    Notes
    -----
    * If an entry with the same ``client_id`` already exists, it is
      replaced only if the new size does not exceed limits.
    * The function acquires a lock to ensure thread safety and
      protects against concurrent modifications.
    """
    if not isinstance(client_id, str) or not client_id:
        # Invalid key – do nothing
        return False

    if not isinstance(client_data, dict):
        # Invalid data – do nothing
        return False

    with cache_lock:
        # Compute new size if we were to insert/update
        existing_size = sys.getsizeof(user_cache[client_id]) if client_id in user_cache else 0
        new_entry_size = sys.getsizeof(client_data)

        projected_total = _current_cache_size() - existing_size + new_entry_size

        # Check size and count limits
        if projected_total > MAX_CACHE_SIZE or (client_id not in user_cache and len(user_cache) >= MAX_CLIENTS):
            return False

        # Safe to add/update
        user_cache[client_id] = client_data
        return True


# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    import random
    for i in range(10):
        cid = f"user_{i}"
        data = {"name": f"User {i}", "score": random.randint(0, 100)}
        success = cache_client_info(cid, data)
        print(f"Cached {cid}: {'Success' if success else 'Failed'}")