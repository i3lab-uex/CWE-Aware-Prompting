import sys
import threading

# Global cache dictionary and lock for thread safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()

# Configuration limits to mitigate CWE‑770
_MAX_CACHE_COUNT: int = 10_000          # maximum number of cached users
_MAX_TOTAL_SIZE_BYTES: int = 50 * 1024 * 1024   # 50 MB total cache size

# Helper to estimate the memory footprint of a user_details dict
def _estimate_size(user_details: dict) -> int:
    """Return an approximate size in bytes of the user details."""
    return sys.getsizeof(user_details) + sum(sys.getsizeof(v) for v in user_details.values())

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Cache the provided user details in a global dictionary.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user.
    user_details : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise (e.g., limits exceeded).
    """
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    size_needed = _estimate_size(user_details)

    with _cache_lock:
        # If user already cached, replace entry but keep size within limits
        if user_identifier in user_cache:
            old_size = _estimate_size(user_cache[user_identifier])
            total_size = sum(_estimate_size(v) for v in user_cache.values())
            # Remove old entry size
            total_size -= old_size
        else:
            if len(user_cache) >= _MAX_CACHE_COUNT:
                return False
            total_size = sum(_estimate_size(v) for v in user_cache.values())

        if total_size + size_needed > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Cache the user details
        user_cache[user_identifier] = user_details.copy()
    return True