#!/usr/bin/env python3
"""
Memory‑based user cache with size limits to mitigate CWE‑770.

The cache is implemented as a thread‑safe LRU (least recently used) store.
When the maximum capacity is reached, the oldest entry is evicted before
inserting a new one. This prevents unbounded memory consumption.
"""

from __future__ import annotations

import collections
import threading
from typing import Dict, Tuple

# --------------------- Configuration ---------------------

# Maximum number of users that can be cached simultaneously.
_MAX_CACHE_SIZE: int = 1000

# --------------------- Global Cache ---------------------

# The cache stores (identifier -> data_info) pairs.
_user_cache: "collections.OrderedDict[str, Dict]" = collections.OrderedDict()

# Lock to protect concurrent access to the cache.
_cache_lock: threading.Lock = threading.Lock()


def store_user_info(identifier: str, data_info: Dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        Dictionary containing arbitrary user-related information.

    Returns
    -------
    bool
        True if the entry was successfully cached; False otherwise.
    """
    # Basic validation to avoid storing non‑dict values
    if not isinstance(identifier, str) or not isinstance(data_info, dict):
        return False

    try:
        with _cache_lock:
            # If the identifier already exists, move it to the end (most recent)
            if identifier in _user_cache:
                _user_cache.move_to_end(identifier)

            # Insert/overwrite the entry
            _user_cache[identifier] = data_info

            # Enforce cache size limit – evict oldest entry if necessary
            if len(_user_cache) > _MAX_CACHE_SIZE:
                # popitem(last=False) removes the first (oldest) item
                _user_cache.popitem(last=False)

        return True

    except Exception:
        # We swallow any exception to adhere to the contract of never raising.
        return False


# --------------------- Utility Functions (Optional) ---------------------

def get_user_info(identifier: str) -> Tuple[bool, Dict | None]:
    """
    Retrieve user information from the cache.

    Parameters
    ----------
    identifier : str
        The unique user identifier.

    Returns
    -------
    tuple[bool, dict | None]
        (found_flag, data_info). If not found, returns (False, None).
    """
    with _cache_lock:
        data = _user_cache.get(identifier)
        if data is None:
            return False, None
        # Move to end to mark as recently used
        _user_cache.move_to_end(identifier)
        return True, data


def cache_size() -> int:
    """Return the current number of cached users."""
    with _cache_lock:
        return len(_user_cache)