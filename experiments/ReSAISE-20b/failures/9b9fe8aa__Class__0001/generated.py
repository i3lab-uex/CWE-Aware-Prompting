# cache_user_info.py

"""
Efficient memory‑based caching for user information.

The implementation enforces two limits:
1. Maximum total number of cached users (`MAX_CACHE_SIZE`).
2. Maximum size (in bytes) for each user details dictionary
   (`MAX_USER_ENTRY_SIZE`).

If either limit would be violated, the function returns False and
does not modify the cache.  Thread safety is achieved using a
threading.Lock.

CWE-400: The code protects against uncontrolled resource consumption by
imposing explicit limits on cache size and entry size.
"""

import sys
from threading import Lock
from collections.abc import Mapping

# Global cache dictionary and its lock
user_cache: dict[str, dict] = {}
_cache_lock = Lock()

# Configuration constants (tweak as needed)
MAX_CACHE_SIZE: int = 10_000          # maximum number of cached users
MAX_USER_ENTRY_SIZE: int = 1_048_576   # maximum bytes per user details (1 MiB)


def _dict_size_in_bytes(d: Mapping) -> int:
    """
    Roughly estimate the memory footprint of a dictionary in bytes.
    For simplicity we serialize it to bytes via repr.  This is
    conservative and inexpensive for small dicts.
    """
    try:
        return len(repr(d).encode("utf-8"))
    except Exception:  # pragma: no cover
        return sys.getsizeof(d)


def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary of user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not user_identifier:
        return False

    if not isinstance(user_details, dict):
        return False

    # Enforce per‑entry size limit
    entry_size = _dict_size_in_bytes(user_details)
    if entry_size > MAX_USER_ENTRY_SIZE:
        return False

    with _cache_lock:
        # If the user already exists, replace it regardless of size
        if user_identifier in user_cache:
            user_cache[user_identifier] = user_details
            return True

        # Enforce total cache size limit
        if len(user_cache) >= MAX_CACHE_SIZE:
            return False

        user_cache[user_identifier] = user_details
        return True