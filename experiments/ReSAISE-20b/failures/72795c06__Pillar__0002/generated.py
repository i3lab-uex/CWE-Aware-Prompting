# cache_profile_data.py

"""
In‑memory caching for user profile data.

The module exposes a single function `cache_profile_data` that stores
profile information in the global dictionary `user_cache`.  The function
validates inputs, uses a lock to make updates thread‑safe and returns a
boolean status indicator.  No exceptions are raised; any failure simply
returns `False`.

The implementation follows best practices for resource control:
* The cache is a simple dictionary; it is never unintentionally
  duplicated or leaked.
* A global lock ensures that concurrent accesses cannot corrupt the
  cache state, preventing race conditions that could lead to resource
  misuse (CWE‑664).
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Global cache dictionary and its lock for thread safety
user_cache: Dict[str, Dict[str, Any]] = {}
_user_cache_lock = threading.RLock()


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user profile in the in‑memory cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing the user's profile details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic input validation – ensure types are correct
    if not isinstance(profile_id, str) or not profile_id:
        return False

    if not isinstance(profile_data, dict):
        return False

    # Use a lock to avoid race conditions in multi‑threaded contexts
    try:
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[profile_id] = dict(profile_data)
        return True
    except Exception:
        # Log the exception in a real application; here we simply suppress it
        return False


# Example usage (for demonstration only – remove in production)
if __name__ == "__main__":
    success = cache_profile_data("user123", {"name": "Alice", "age": 30})
    print(f"Cache operation successful: {success}")
    print("Current cache state:", user_cache)