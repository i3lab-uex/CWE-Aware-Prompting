# cache_profile_data.py

"""
In‑memory user profile caching with basic size control to mitigate
CWE‑400: Uncontrolled Resource Consumption.
"""

from collections import OrderedDict
from typing import Dict

# Global cache with a maximum capacity to prevent uncontrolled growth.
MAX_CACHE_SIZE = 10_000  # adjust as appropriate for the deployment environment
user_cache: "OrderedDict[str, Dict]" = OrderedDict()


def cache_profile_data(profile_id: str, profile_data: Dict) -> bool:
    """
    Stores or updates the user profile data in an in‑memory cache.

    Parameters
    ----------
    profile_id : str
        Unique identifier for the user profile.
    profile_data : dict
        Dictionary containing profile details.

    Returns
    -------
    bool
        True if the operation succeeds, False otherwise.
    """
    try:
        # If profile already exists, move it to the end (most recently used)
        if profile_id in user_cache:
            user_cache.move_to_end(profile_id)

        # Insert or update the profile data
        user_cache[profile_id] = profile_data

        # Evict oldest entries if cache exceeds the maximum size
        while len(user_cache) > MAX_CACHE_SIZE:
            # popitem(last=False) removes the oldest item
            user_cache.popitem(last=False)

        return True

    except Exception:
        # In a real-world scenario we might log the exception here.
        return False