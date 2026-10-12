import json
from typing import Dict

# Global cache dictionary
user_cache: Dict[str, dict] = {}

# Configuration for limits
MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024   # 10 MB total cache size
MAX_USER_COUNT = 1000                     # maximum number of cached users

def _current_cache_size() -> int:
    """Return the current total size in bytes of all cached user details."""
    return sum(len(json.dumps(details).encode('utf-8')) for details in user_cache.values())

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if caching succeeded, False if it would exceed limits.
    """
    # Serialize once to measure size
    try:
        serialized = json.dumps(user_details)
    except (TypeError, ValueError):
        # Cannot serialize; treat as failure
        return False

    entry_size = len(serialized.encode('utf-8'))

    # Check user count limit
    if user_identifier not in user_cache and len(user_cache) >= MAX_USER_COUNT:
        return False

    # Check size limit
    current_size = _current_cache_size()
    if user_identifier not in user_cache:
        # New entry
        if current_size + entry_size > MAX_CACHE_SIZE_BYTES:
            return False
    else:
        # Replacing existing; size change may be positive or negative
        old_size = len(json.dumps(user_cache[user_identifier]).encode('utf-8'))
        if current_size - old_size + entry_size > MAX_CACHE_SIZE_BYTES:
            return False

    # All checks passed; store the user data
    user_cache[user_identifier] = user_details
    return True