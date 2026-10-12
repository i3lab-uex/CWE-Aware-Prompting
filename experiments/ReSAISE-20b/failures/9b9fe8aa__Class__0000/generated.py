import sys
import threading

# Global cache and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Configuration limits (adjust as needed)
_MAX_ENTRIES = 1_000                # Maximum number of cached users
_MAX_CACHE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB total cache size

def _current_cache_size() -> int:
    """Return the approximate memory footprint of the cache in bytes."""
    # Use sys.getsizeof on each user detail dict; this is an estimate.
    return sum(sys.getsizeof(v) for v in user_cache.values())

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store user information in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary of user attributes.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (due to limits).
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not user_identifier:
        return False
    if not isinstance(user_details, dict):
        return False

    with _user_cache_lock:
        # If the entry already exists, replace it (no size penalty)
        if user_identifier in user_cache:
            user_cache[user_identifier] = user_details
            return True

        # Enforce entry count limit
        if len(user_cache) >= _MAX_ENTRIES:
            return False

        # Estimate new size
        estimated_size = _current_cache_size() + sys.getsizeof(user_details)
        if estimated_size > _MAX_CACHE_SIZE_BYTES:
            return False

        # Add to cache
        user_cache[user_identifier] = user_details
        return True