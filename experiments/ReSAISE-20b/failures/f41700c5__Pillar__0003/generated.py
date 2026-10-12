# -*- coding: utf-8 -*-

"""
Memory-based caching system for user data.
The module defines a global dictionary `user_cache` that stores
user-specific information keyed by a unique identifier.  The function
`store_user_info()` safely inserts or updates entries in this cache.

Security considerations:
* The function validates that the key is a non-empty string and that
  the value is a dictionary to prevent accidental cache corruption.
* A threading lock protects concurrent access, mitigating race conditions
  and potential denial‑of‑service scenarios (CWE‑664: Improper Control of a
  Resource Through its Lifetime).
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its associated lock
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Store or update user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        A unique string that identifies each user.
    data_info : dict
        Dictionary containing various user-related information.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation to avoid corrupting the cache
    if not isinstance(identifier, str) or not identifier:
        return False

    if not isinstance(data_info, dict):
        return False

    # Use a re‑entrant lock to allow nested calls from the same thread
    try:
        with _user_cache_lock:
            # Store or update the entry atomically
            user_cache[identifier] = data_info.copy()
    except Exception:
        # Swallow exceptions to keep the API contract simple
        return False

    return True