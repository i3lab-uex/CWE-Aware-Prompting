#!/usr/bin/env python3
"""
Memory‑based user cache implementation.

This module provides a thread‑safe function `store_user_data` that stores
user information in an in‑memory dictionary (`user_cache`).  The cache has a
maximum entry count and maximum total size in bytes; attempts to exceed these
limits fail gracefully.

The implementation deliberately avoids external dependencies and uses only
the Python standard library.
"""

from __future__ import annotations

import threading
import sys
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration constants – adjust as needed for the target environment
# --------------------------------------------------------------------------- #

# Maximum number of users that can be cached simultaneously.
MAX_CACHE_ENTRIES: int = 10_000

# Maximum total memory footprint (bytes) for all cached user data.
# This is a *rough* estimate; we use sys.getsizeof to approximate each entry.
MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MB

# --------------------------------------------------------------------------- #
# Global cache and synchronization primitives
# --------------------------------------------------------------------------- #

user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.RLock()


def _current_cache_size() -> int:
    """
    Compute the approximate memory usage of the cache.

    Returns:
        int: Total size in bytes.
    """
    total = 0
    for uid, data in user_cache.items():
        # Include the size of the key and the dictionary object itself.
        total += sys.getsizeof(uid) + sys.getsizeof(data)
        # Also account for the sizes of all nested objects.
        total += sum(sys.getsizeof(v) for v in data.values())
    return total


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def store_user_data(uid: str, data: Dict[str, Any]) -> bool:
    """
    Store user information in the global `user_cache`.

    The function ensures that adding a new entry does not violate cache
    size or count limits.  It is safe to call from multiple threads.

    Args:
        uid: Unique string identifier for the user.
        data: Dictionary of attributes related to the user.

    Returns:
        bool: True if the entry was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Compute the size of the new entry
    estimated_entry_size = (
        sys.getsizeof(uid) + sys.getsizeof(data)
        + sum(sys.getsizeof(v) for v in data.values())
    )

    with _cache_lock:
        # If the entry already exists, we treat it as a replacement
        if uid in user_cache:
            # Remove old size contribution first
            old_entry_size = (
                sys.getsizeof(uid) + sys.getsizeof(user_cache[uid])
                + sum(sys.getsizeof(v) for v in user_cache[uid].values())
            )
            total_size = _current_cache_size() - old_entry_size + estimated_entry_size
        else:
            total_size = _current_cache_size() + estimated_entry_size

        # Check count and size limits
        if len(user_cache) >= MAX_CACHE_ENTRIES and uid not in user_cache:
            return False
        if total_size > MAX_CACHE_SIZE_BYTES:
            return False

        # Store the data (replace existing entry if present)
        user_cache[uid] = data.copy()

    return True


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only – remove or guard under `if __name__ == "__main__":`)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple sanity check
    assert store_user_data("user1", {"name": "Alice", "age": 30}) is True
    assert store_user_data("user2", {"name": "Bob", "age": 25}) is True
    print(f"Cache size: {len(user_cache)} entries")