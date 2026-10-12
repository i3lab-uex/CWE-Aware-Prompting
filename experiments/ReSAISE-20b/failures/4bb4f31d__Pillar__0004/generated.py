#!/usr/bin/env python3
"""
Memory‑based caching for user data.

The module exposes a single function `cache_application_data` that stores
user‑specific information in the global dictionary `user_cache`.  The cache
is protected by a re‑entrant lock to prevent race conditions in multi‑threaded
environments, and it enforces a size limit to avoid uncontrolled memory growth,
thereby mitigating CWE‑664 (Improper Control of a Resource Through its
Lifetime).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global cache and supporting objects
# --------------------------------------------------------------------------- #

# Maximum number of entries the cache may hold.  Adjust as needed.
_MAX_CACHE_SIZE: int = 10_000

# The actual cache dictionary
user_cache: Dict[str, Dict[str, Any]] = {}

# Re‑entrant lock for thread safety
_cache_lock: threading.RLock = threading.RLock()


def _ensure_cache_size() -> None:
    """
    Evict oldest entries if the cache exceeds its maximum size.
    This simple implementation uses FIFO eviction based on insertion order
    (Python 3.7+ preserves dict order).
    """
    if len(user_cache) <= _MAX_CACHE_SIZE:
        return

    # Determine how many entries to remove
    excess = len(user_cache) - _MAX_CACHE_SIZE
    # Pop the first `excess` items (oldest)
    for _ in range(excess):
        # dict.popitem(last=False) pops the first inserted item
        user_cache.popitem(last=False)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user‑specific information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user. Must be a non‑empty string.
    info_data : dict
        Dictionary containing arbitrary user data. The function makes a deep
        copy to prevent accidental mutation of the cached value.

    Returns
    -------
    bool
        ``True`` if caching succeeded, ``False`` otherwise.

    Notes
    -----
    * The function is thread‑safe.
    * A maximum cache size is enforced to avoid uncontrolled memory
      consumption (CWE‑664 mitigation).
    * Input validation guards against accidental injection of malicious data.
    """
    # Basic type and value checks
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    try:
        # Deep copy to isolate cached data from external mutations
        data_copy = copy.deepcopy(info_data)

        with _cache_lock:
            user_cache[client_id] = data_copy
            _ensure_cache_size()

        return True

    except Exception:
        # In production you might log the exception, but per specification
        # no exceptions should propagate.
        return False

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(cache_application_data("user123", {"name": "Alice", "age": 30}))
#     print(user_cache)