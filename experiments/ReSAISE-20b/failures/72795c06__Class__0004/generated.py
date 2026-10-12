# -*- coding: utf-8 -*-
"""
In‑memory caching for user profiles with a simple size guard.
"""

from typing import Dict, Any

# Global cache dictionary.  Keys are profile_id strings,
# values are the corresponding profile_data dictionaries.
user_cache: Dict[str, Dict[str, Any]] = {}

# Maximum number of cached entries to mitigate uncontrolled resource consumption.
MAX_CACHE_SIZE: int = 10000


def cache_profile_data(profile_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Store a user's profile data in the global cache.

    Parameters
    ----------
    profile_id : str
        A unique identifier for the user.
    profile_data : dict
        The data to cache for this user.

    Returns
    -------
    bool
        True if the profile was cached successfully, False otherwise.
    """
    # Basic validation: ensure the key is a string and data is a dictionary
    if not isinstance(profile_id, str) or not isinstance(profile_data, dict):
        return False

    # Enforce a maximum cache size to avoid uncontrolled growth
    if len(user_cache) >= MAX_CACHE_SIZE:
        # Optionally: evict the least recently used item or simply refuse new entries.
        # Here we simply reject to keep implementation straightforward.
        return False

    try:
        user_cache[profile_id] = profile_data
        return True
    except Exception:
        # Any unexpected exception should not crash the application.
        return False