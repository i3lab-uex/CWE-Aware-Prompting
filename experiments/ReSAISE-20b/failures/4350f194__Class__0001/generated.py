# user_cache.py

"""
A simple in‑memory cache for user data.

The cache is intentionally small to avoid uncontrolled resource
consumption (CWE‑400).  If the cache exceeds `MAX_CACHE_SIZE` entries,
the oldest entry is evicted before adding a new one.
"""

from collections import OrderedDict
from typing import Dict, Any

# Global cache with a maximum size.
MAX_CACHE_SIZE = 10_000
user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()


def cache_user_data(user_id: str, user_data: Dict[str, Any]) -> bool:
    """
    Store a user's data in the global cache.

    Parameters
    ----------
    user_id : str
        Unique identifier for the user.
    user_data : dict
        Dictionary containing user information.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    # Evict the oldest entry if we are at capacity
    if len(user_cache) >= MAX_CACHE_SIZE:
        # popitem(last=False) removes the first inserted item
        user_cache.popitem(last=False)

    # Store or update the entry
    user_cache[user_id] = user_data
    return True


# Optional helper: retrieve cached data (not required by the spec)
def get_cached_user(user_id: str) -> Dict[str, Any] | None:
    """
    Retrieve a cached user entry if present.

    Parameters
    ----------
    user_id : str

    Returns
    -------
    dict or None
        The cached user data, or None if not found.
    """
    return user_cache.get(user_id)