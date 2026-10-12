# -*- coding: utf-8 -*-

"""
Memory‑based caching module for user data.
Implements a simple, thread‑safe cache with configurable limits to mitigate
CWE‑770 (uncontrolled resource allocation).
"""

import threading
from collections import OrderedDict
from typing import Dict, Any

# Global cache and configuration constants
USER_CACHE_MAX_ENTRIES: int = 10_000          # Maximum number of cached users
USER_CACHE_MAX_SIZE_BYTES: int = 50 * 1024**2  # Rough maximum size (~50 MiB)

# Thread‑safe, ordered dictionary to keep track of insertion order for eviction
_user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
_cache_lock = threading.RLock()


def _current_cache_size_bytes() -> int:
    """
    Estimate the current memory usage of the cache by summing the sizes
    of keys and values.  This is a heuristic; for production use a
    dedicated memory‑profiling library.
    """
    size = 0
    for key, value in _user_cache.items():
        size += len(key.encode("utf-8"))
        try:
            import sys
            size += sys.getsizeof(value)
        except Exception:  # pragma: no cover
            pass
    return size


def _enforce_limits() -> bool:
    """
    Evict the oldest entries until both size and entry limits are respected.
    Returns True if eviction succeeded, False otherwise (e.g. if an item
    is too large to fit even when the cache is empty).
    """
    while True:
        with _cache_lock:
            if len(_user_cache) <= USER_CACHE_MAX_ENTRIES and \
               _current_cache_size_bytes() <= USER_CACHE_MAX_SIZE_BYTES:
                return True

            if not _user_cache:  # Nothing to evict
                return False

            # Evict the oldest entry (FIFO)
            _, _ = _user_cache.popitem(last=False)


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    info_data : dict
        Dictionary containing arbitrary user data.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    if not isinstance(client_id, str) or not client_id:
        return False

    if not isinstance(info_data, dict):
        return False

    with _cache_lock:
        # If the client is already cached, update and move to end
        if client_id in _user_cache:
            _user_cache.pop(client_id)
        _user_cache[client_id] = info_data

    # Enforce cache limits; if eviction fails, remove the just-added entry
    if not _enforce_limits():
        with _cache_lock:
            _user_cache.pop(client_id, None)
        return False

    return True