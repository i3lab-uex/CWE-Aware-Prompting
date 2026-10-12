# cache_profile_data.py

"""
An in‑memory caching mechanism for user profiles.
The cache is an LRU (Least Recently Used) store with a configurable maximum size
to mitigate CWE‑400: Uncontrolled Resource Consumption.
"""

from collections import OrderedDict
from typing import Dict, Any

# Global cache instance (LRU order preserved)
user_cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()

# Maximum number of cached entries (adjust as needed)
_MAX_CACHE_SIZE: int = 1000


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Stores the given user profile data in the global cache.

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
    # Basic type validation – avoid corrupting the cache
    if not isinstance(profile_id, str) or not isinstance(profile_data, dict):
        return False

    # If the key already exists, update its position (most recently used)
    if profile_id in user_cache:
        # Remove and re‑insert to move it to the end
        del user_cache[profile_id]
    elif len(user_cache) >= _MAX_CACHE_SIZE:
        # Evict the least‑recently used item
        user_cache.popitem(last=False)

    try:
        user_cache[profile_id] = profile_data
        return True
    except Exception:
        # Any unexpected error (unlikely with dict operations) results in failure
        return False


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Populate cache with dummy data
    for i in range(5):
        assert cache_profile_data(f"user_{i}", {"name": f"User {i}", "age": 20 + i})
    print("Cache contents:", user_cache)