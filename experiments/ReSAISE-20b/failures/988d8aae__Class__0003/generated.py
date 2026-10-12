#!/usr/bin/env python3
"""
A lightweight, memory‑constrained cache for per‑client data.
"""

import json
import sys
from threading import RLock

# --------------------------------------------------------------------------- #
# Configuration – tune these values to match the target environment
# --------------------------------------------------------------------------- #

# Maximum total size of all cached entries combined (bytes)
MAX_TOTAL_CACHE_BYTES = 50 * 1024 * 1024   # 50 MiB

# Maximum number of entries that can be stored
MAX_CACHE_ENTRIES = 10_000

# --------------------------------------------------------------------------- #
# Global cache store and associated lock for thread safety
# --------------------------------------------------------------------------- #

user_cache: dict[str, dict] = {}
_cache_lock = RLock()


def _current_cache_size() -> int:
    """Return the current size of the cache in bytes."""
    total = 0
    for data in user_cache.values():
        # Estimate size by serialising to JSON (deterministic and fast)
        try:
            total += len(json.dumps(data).encode("utf-8"))
        except Exception:
            # Fallback to sys.getsizeof if JSON fails
            total += sys.getsizeof(data)
    return total


def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store the supplied `client_data` under `client_id` in the global cache.

    The function enforces two constraints:
        1. Total size of all cached data must not exceed `MAX_TOTAL_CACHE_BYTES`.
        2. Number of entries in the cache must not exceed `MAX_CACHE_ENTRIES`.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        ``True`` if the entry was cached successfully, ``False`` otherwise.
    """
    # Basic validation
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    # Estimate the size of the new entry
    try:
        entry_size = len(json.dumps(client_data).encode("utf-8"))
    except Exception:
        entry_size = sys.getsizeof(client_data)

    with _cache_lock:
        # Enforce entry count limit
        if len(user_cache) >= MAX_CACHE_ENTRIES and client_id not in user_cache:
            return False

        # Enforce total size limit
        current_size = _current_cache_size()
        projected_size = current_size + entry_size - (
            len(json.dumps(user_cache.get(client_id, {})).encode("utf-8"))
            if client_id in user_cache
            else 0
        )
        if projected_size > MAX_TOTAL_CACHE_BYTES:
            return False

        # Cache the data
        user_cache[client_id] = client_data.copy()

    return True


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample client data
    for i in range(5):
        cid = f"user_{i}"
        data = {"name": f"User {i}", "age": 20 + i, "roles": ["user", "admin"] if i % 2 == 0 else ["user"]}
        success = cache_client_info(cid, data)
        print(f"Caching {cid}: {'Success' if success else 'Failed'}")

    # Inspect cache
    print("\nCached entries:")
    for cid, data in user_cache.items():
        print(f"  {cid}: {data}")