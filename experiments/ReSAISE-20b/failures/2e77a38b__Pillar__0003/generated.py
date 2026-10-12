# memory_cache.py

"""
Memory-based caching system for user data.

This module provides a simple in‑memory cache that stores user information
using a globally shared dictionary. The implementation is thread‑safe and
ensures that the cache is not corrupted by concurrent writes.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by:
  • Using a global lock to serialize access to the shared cache.
  • Performing minimal validation on inputs before caching.
"""

import threading
from typing import Dict, Any

# Global cache dictionary and lock for thread‑safety.
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    cust_id : str
        A unique string that identifies each user.
    cust_data : dict
        Dictionary containing various user-related information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.

    Notes
    -----
    - The function is thread‑safe; concurrent calls are serialized by a lock.
    - Input validation is minimal: `cust_id` must be a non‑empty string and
      `cust_data` must be a dictionary.  All other checks are left to the caller.
    - No size limit is imposed on the cache; in a production system you would
      want to implement eviction policies or persistence.
    """
    # Basic input validation
    if not isinstance(cust_id, str) or not cust_id:
        return False
    if not isinstance(cust_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to prevent accidental external mutation
            user_cache[cust_id] = dict(cust_data)
        return True
    except Exception:
        # In case of any unexpected error (unlikely with a dict), return False
        return False