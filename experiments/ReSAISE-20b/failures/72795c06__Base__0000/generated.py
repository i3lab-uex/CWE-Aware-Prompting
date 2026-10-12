# -*- coding: utf-8 -*-
"""
In‑memory cache for user profile data.

The cache is a simple dictionary that maps a unique profile_id to its
corresponding profile_data.  To mitigate CWE‑770 (unbounded allocation of
resources), the cache enforces a maximum size.  When the limit is reached,
new entries are rejected until space becomes available.
"""

from __future__ import annotations

# Global cache dictionary
user_cache: dict[str, dict] = {}

# Maximum number of entries allowed in the cache.
MAX_CACHE_SIZE: int = 10_000

def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store the given profile data in the global cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user.
    profile_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the entry was cached successfully; False otherwise.
    """
    # Basic validation: profile_id must be a non-empty string
    if not isinstance(profile_id, str) or not profile_id:
        return False

    # Ensure the data is a dictionary
    if not isinstance(profile_data, dict):
        return False

    # Enforce cache size limit
    if len(user_cache) >= MAX_CACHE_SIZE:
        return False

    # Store or update the entry
    user_cache[profile_id] = profile_data.copy()
    return True