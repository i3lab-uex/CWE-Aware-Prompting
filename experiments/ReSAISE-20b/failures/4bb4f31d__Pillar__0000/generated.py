# -*- coding: utf-8 -*-
"""
A simple in‑memory cache for user data.

The cache is a global dictionary protected by a threading lock to avoid
concurrent write issues.  The function ``cache_application_data`` stores
user‑specific data and returns ``True`` on success, otherwise ``False``.

CWE-664: The implementation guarantees that the cache dictionary is
created once, used safely across threads, and never closed or
invalidated during the application's lifetime.  This mitigates improper
control of a resource through its lifetime.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its lock.
user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = threading.Lock()


def cache_application_data(client_id: str, info_data: Dict[str, Any]) -> bool:
    """
    Store user data in the global ``user_cache`` dictionary.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    info_data : dict
        Dictionary containing user‑related information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, ``False`` otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    try:
        # Acquire the lock to prevent race conditions.
        with _cache_lock:
            user_cache[client_id] = info_data.copy()
        return True
    except Exception:  # pragma: no cover
        # In a real application you might log the exception.
        return False


# Example usage (for demonstration only; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    result = cache_application_data("user123", {"name": "Alice", "role": "admin"})
    print(f"Cache successful: {result}")  # Expected: True
    print(user_cache)