# -*- coding: utf-8 -*-

"""
Memory‑based caching system for user data.

The module defines a global dictionary `user_cache` that stores
customer information indexed by their unique identifier.
The function `store_customer_info` validates inputs and updates the
cache. Thread safety is ensured using a lock to prevent race
conditions in concurrent environments.
"""

from __future__ import annotations

import threading
from typing import Dict, Any, Optional


# Global cache dictionary
user_cache: Dict[str, Dict[str, Any]] = {}

# Lock to protect access to the cache
_cache_lock = threading.RLock()


def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Store customer data in the global `user_cache`.

    Parameters
    ----------
    cust_id : str
        A unique string that identifies each user.
    cust_data : dict
        Dictionary containing user-related information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``.

    Notes
    -----
    - The function performs basic type checking; if the arguments are not
      of the expected types, it returns ``False``.
    - A re‑entrant lock is used to ensure that concurrent writes do not
      corrupt the cache, mitigating CWE-664 (improper control of a
      resource through its lifetime).
    - No external resources are opened, so there is no need for explicit
      cleanup.
    """
    # Basic validation of inputs
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    try:
        with _cache_lock:
            # Store or update the entry in the cache
            user_cache[cust_id] = cust_data.copy()
        return True
    except Exception:
        # Any unexpected exception results in a failure indicator
        return False