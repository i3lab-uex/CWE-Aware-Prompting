#!/usr/bin/env python3
"""
Efficient memory‑based caching for user information.

This module implements a simple thread‑safe cache that stores
user details in a global dictionary.  The cache enforces limits on:
* the maximum number of cached entries (`MAX_CACHE_COUNT`)
* the approximate total memory footprint in bytes
  (`MAX_CACHE_SIZE_BYTES`).

The `cache_user_info` function returns ``True`` when a user entry is
successfully cached, otherwise ``False`` (e.g. if the cache would exceed
the configured limits).

Security considerations:
* The cache is purely in‑memory; no persistent storage or serialization
  occurs, so there are no injection concerns.
* The function does not expose any sensitive data; it only stores the
  provided ``user_details`` dictionary as is.
* Thread safety is ensured via a global lock, preventing race
  conditions that could otherwise corrupt the cache or its size tracking.
"""

import sys
import threading
from typing import Dict, Any

# Global cache dictionary and lock for thread safety.
user_cache: Dict[str, Dict[str, Any]] = {}
cache_lock = threading.Lock()

# Configuration constants – adjust as needed for your environment.
MAX_CACHE_COUNT: int = 10_000          # maximum number of cached users
MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024  # ~50 MB

# Helper to estimate the size of a dictionary entry in bytes.
def _estimate_entry_size(user_details: Dict[str, Any]) -> int:
    """Return an approximate memory footprint of a user_details dict."""
    size = sys.getsizeof(user_details)
    for key, value in user_details.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def cache_user_info(user_identifier: str, user_details: Dict[str, Any]) -> bool:
    """
    Store or update a user's details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        ``True`` if the cache was updated successfully.
        ``False`` if adding/updating would exceed size/count limits.

    Notes
    -----
    * The function is idempotent: if the user already exists,
      its entry is replaced, and size bookkeeping accounts for
      the difference between old and new sizes.
    * No exceptions are raised; failures are indicated via the boolean
      return value.
    """
    # Quick sanity check on input types (fails silently by returning False).
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    entry_size = _estimate_entry_size(user_details)

    with cache_lock:
        # Determine current size of the user entry if it already exists.
        old_entry_size = _estimate_entry_size(user_cache.get(user_identifier, {}))
        # Compute new total size if we replace/add this entry.
        current_total_size = sum(
            _estimate_entry_size(details) for details in user_cache.values()
        )
        new_total_size = current_total_size - old_entry_size + entry_size

        # Check count limit if adding a new entry.
        is_new = user_identifier not in user_cache
        current_count = len(user_cache)
        new_count = current_count + (1 if is_new else 0)

        # Enforce limits
        if new_total_size > MAX_CACHE_SIZE_BYTES or new_count > MAX_CACHE_COUNT:
            return False

        # Perform the cache update.
        user_cache[user_identifier] = user_details
    return True