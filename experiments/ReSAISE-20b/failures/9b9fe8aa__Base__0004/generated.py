# -*- coding: utf-8 -*-
"""
A lightweight, memory‑based cache for user information.

The implementation protects against unbounded growth (CWE‑770) by
enforcing configurable limits on the total memory footprint and the
maximum number of cached entries.  The cache is protected by a lock
to make it safe for concurrent access in multi‑threaded environments.
"""

import threading
from collections.abc import Mapping

# Global cache dictionary and associated lock
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
_MAX_CACHE_ENTRIES: int = 10_000          # maximum number of cached users
_MAX_TOTAL_SIZE_BYTES: int = 50 * 1024 ** 2  # ~50 MiB total size

def _approximate_size(obj: Mapping) -> int:
    """
    Roughly estimate the memory size of a dictionary object.
    This is a heuristic; for more accurate measurement `sys.getsizeof`
    can be used recursively, but that would be slower.
    """
    size = 0
    for k, v in obj.items():
        # Rough estimate: key + value sizes plus overhead
        size += len(str(k)) * 2      # rough bytes for key string
        if isinstance(v, str):
            size += len(v) * 2      # rough bytes for string value
        else:
            size += 64              # generic object overhead estimate
    return size

def cache_user_info(user_identifier: str, user_details: Mapping) -> bool:
    """
    Cache user information in a global dictionary.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : Mapping
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully; False otherwise
        (e.g., when cache limits would be exceeded).
    """
    if not isinstance(user_identifier, str):
        return False
    if not isinstance(user_details, Mapping):
        return False

    # Estimate the size of the new entry
    new_entry_size = _approximate_size(user_details)

    with _cache_lock:
        # If the user is already cached, we allow overwrite
        existing_size = _approximate_size(user_cache.get(user_identifier, {}))

        # Compute prospective total size
        current_total_size = sum(_approximate_size(v) for v in user_cache.values())
        prospective_size = current_total_size - existing_size + new_entry_size

        # Check limits
        if len(user_cache) >= _MAX_CACHE_ENTRIES and user_identifier not in user_cache:
            return False
        if prospective_size > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Perform the cache update
        user_cache[user_identifier] = dict(user_details)

    return True