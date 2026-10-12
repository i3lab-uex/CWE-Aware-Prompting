# -*- coding: utf-8 -*-
"""
Simple in‑memory user data cache.

This module exposes a single function `cache_user_data` which stores
user information in a global dictionary.  The implementation protects
against concurrent access using a thread lock and validates input to
avoid accidental storage of malformed data.

Security considerations:
- Input is validated: `user_id` must be a non‑empty string and
  `user_data` must be a dictionary.
- The cache is not exposed to external mutation; callers receive
  no reference to the internal dictionary.
- The cache is cleared on import of this module; it does not persist
  beyond the lifetime of the process.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary protected by a lock to prevent race conditions.
_user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store the provided `user_data` in an in‑memory cache keyed by `user_id`.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user. Must be a non‑empty string.
    user_data : dict
        Dictionary containing user information. Must not be empty.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``.

    Notes
    -----
    The function performs minimal validation:
        * `user_id` must be a non‑empty string.
        * `user_data` must be a dictionary with at least one key.

    The global cache is thread‑safe: all modifications occur while holding
    a lock to avoid race conditions and ensure consistency.
    """
    # Basic input validation
    if not isinstance(user_id, str) or not user_id:
        return False

    if not isinstance(user_data, dict) or not user_data:
        return False

    # Store data atomically
    try:
        with _cache_lock:
            # Make a shallow copy to avoid accidental external mutation
            _user_cache[user_id] = dict(user_data)
        return True
    except Exception:
        # In a real application, log the exception here.
        return False


# Optional helper to retrieve cached data (not part of required API)
def get_cached_user_data(user_id: str) -> Dict[str, Any] | None:
    """
    Retrieve cached user data for a given `user_id`.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict or None
        A copy of the cached data if present, otherwise ``None``.
    """
    with _cache_lock:
        data = _user_cache.get(user_id)
        return dict(data) if data is not None else None