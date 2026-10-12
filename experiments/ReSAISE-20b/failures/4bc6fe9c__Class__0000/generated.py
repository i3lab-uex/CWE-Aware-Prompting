#!/usr/bin/env python3
"""
Memory‑based user cache implementation.

This module defines a global `user_cache` dictionary that stores
per‑user data keyed by a unique string identifier (`uid`).  The
`store_user_data()` function validates the input, checks against
predefined limits (maximum number of cached users and total memory
footprint), and stores the data if allowed.

Security considerations:
- The cache is bounded to prevent uncontrolled memory growth
  (CWE‑400).
- Thread safety is provided via a reentrant lock.
"""

import sys
import threading
from typing import Dict

# --------------------------------------------------------------------------- #
# Global cache and configuration parameters
# --------------------------------------------------------------------------- #

# Maximum number of users that can be cached simultaneously.
_MAX_CACHE_SIZE: int = 10_000

# Maximum total memory usage for the cache (bytes). Rough estimate.
_MAX_TOTAL_BYTES: int = 50 * 1024 * 1024  # 50 MiB

# Global cache dictionary.
user_cache: Dict[str, dict] = {}

# Lock to protect concurrent access to the cache.
_cache_lock = threading.RLock()


def _current_total_bytes() -> int:
    """Estimate the total memory usage of all cached user dictionaries."""
    return sum(sys.getsizeof(v) for v in user_cache.values())


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific data in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user. Must be a non‑empty string.
    data : dict
        Dictionary containing user attributes and details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
        Failure can occur when the cache would exceed configured
        size or count limits.

    Notes
    -----
    - The function does not raise exceptions; any validation errors
      simply result in a return value of False.
    - Thread safety is ensured via an internal re‑entrant lock.
    """
    # Basic validation
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    with _cache_lock:
        # If the uid already exists, we allow overwrite but still
        # enforce limits on total size.  We compute the new size
        # difference to avoid double counting.
        current_bytes = _current_total_bytes()
        new_entry_size = sys.getsizeof(data)

        # If replacing an existing entry, subtract its size.
        if uid in user_cache:
            current_bytes -= sys.getsizeof(user_cache[uid])

        # Check count limit
        if uid not in user_cache and len(user_cache) >= _MAX_CACHE_SIZE:
            return False

        # Check total size limit
        if current_bytes + new_entry_size > _MAX_TOTAL_BYTES:
            return False

        # Store the data
        user_cache[uid] = data
        return True


# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Simple demonstration
    success = store_user_data("user123", {"name": "Alice", "age": 30})
    print(f"Cache store successful: {success}")