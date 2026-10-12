#!/usr/bin/env python3
"""
Memory‑based caching for user information.

This module implements a thread‑safe cache with configurable limits to
mitigate the risk of uncontrolled memory consumption (CWE‑770).
"""

import threading
from typing import Dict, Any

# Global cache dictionary.  Keys are client IDs and values are the
# corresponding client data dictionaries.
user_cache: Dict[str, Dict[str, Any]] = {}

# Lock to guard concurrent access to the cache.
_cache_lock = threading.RLock()

# Configuration limits
_MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024   # 50 MiB
_MAX_CACHE_ENTRIES: int = 10_000                # Maximum number of cached users

def _current_cache_size() -> int:
    """
    Estimate the current size of the cache in bytes.
    Uses sys.getsizeof for a rough approximation.
    """
    import sys
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def cache_client_info(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store or update the user data in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    client_data : dict
        Dictionary containing the user's attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully.
        False if adding it would exceed configured size or count limits.

    Notes
    -----
    - The function is thread‑safe.
    - No exceptions are raised; the caller should check the return value.
    """
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        # Basic type safety; silently fail to avoid leaking information.
        return False

    with _cache_lock:
        # If the client is already cached, we simply replace its data.
        # This may increase size but will not exceed limits if the new
        # entry is smaller or equal in size.
        tentative_cache = user_cache.copy()
        tentative_cache[client_id] = client_data

        # Enforce entry count limit
        if len(tentative_cache) > _MAX_CACHE_ENTRIES:
            return False

        # Enforce size limit
        if _current_cache_size() > _MAX_CACHE_SIZE_BYTES:
            return False

        # Commit the change
        user_cache[client_id] = client_data
        return True