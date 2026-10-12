# -*- coding: utf-8 -*-

"""
In‑memory cache for user profile data.

The module defines a global dictionary `user_cache` that holds
profile information keyed by a unique profile identifier.
"""

from copy import deepcopy
from typing import Dict

# Global cache dictionary
user_cache: Dict[str, Dict] = {}


def cache_profile_data(profile_id: str, profile_data: Dict) -> bool:
    """
    Store a user's profile data in the global cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user profile.
    profile_data : dict
        Dictionary containing profile information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully,
        ``False`` otherwise.
    """
    try:
        # Defensive copy to avoid accidental mutation of the caller's dict
        user_cache[profile_id] = deepcopy(profile_data)
        return True
    except Exception:
        # Log the error in a real application; here we simply swallow it.
        return False