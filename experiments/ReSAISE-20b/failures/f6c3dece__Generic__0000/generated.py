# -*- coding: utf-8 -*-
"""
In‑memory caching for user data.

This module provides a thread‑safe helper function that stores
client information in a global dictionary.  The cache is intended for
short‑lived, read‑heavy scenarios where frequent database lookups would
be costly.  The implementation is deliberately simple but protects
against common pitfalls such as concurrent writes and accidental mutation
of cached values.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_client_data(client_id: str, client_data: Dict[str, Any]) -> bool:
    """
    Store user information in the global `user_cache`.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user (e.g., a UUID or database primary key).
    client_data : dict
        A dictionary containing user‑specific data that should be cached.

    Returns
    -------
    bool
        ``True`` if the caching succeeded, ``False`` otherwise.

    Notes
    -----
    - The function performs a shallow copy of `client_data` to prevent external
      mutations from affecting the cached value.
    - Thread safety is guaranteed by a re‑entrant lock; this allows nested
      calls from the same thread without deadlocking.
    - No exceptions are propagated; failures return ``False`` for
      graceful degradation in calling code.
    """
    try:
        if not isinstance(client_id, str):
            # Client ID must be a string; otherwise we consider it invalid.
            return False

        if not isinstance(client_data, dict):
            # Only dictionaries are accepted for caching.
            return False

        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation.
            user_cache[client_id] = client_data.copy()

        return True
    except Exception:
        # Log the exception in a real application; here we silently fail.
        return False