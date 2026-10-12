import sys
import threading

# Global cache dictionary
user_cache: dict[str, dict] = {}

# Configuration for resource limits
MAX_CACHE_ENTRIES = 10_000          # maximum number of users in cache
MAX_TOTAL_SIZE_BYTES = 50 * 1024 * 1024  # maximum total size of cached data (~50 MB)

# Thread‑safety lock
_cache_lock = threading.RLock()


def _current_total_size() -> int:
    """Return the current total size in bytes of all cached data."""
    return sum(sys.getsizeof(v) for v in user_cache.values())


def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for a user.
    data : dict
        Dictionary containing the user's attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(uid, str) or not uid:
        return False
    if not isinstance(data, dict):
        return False

    # Estimate size of the new entry
    new_entry_size = sys.getsizeof(data)

    with _cache_lock:
        # Enforce entry count limit
        if len(user_cache) >= MAX_CACHE_ENTRIES and uid not in user_cache:
            return False

        # Enforce total size limit
        current_size = _current_total_size()
        if uid not in user_cache:
            # New entry will increase size
            if current_size + new_entry_size > MAX_TOTAL_SIZE_BYTES:
                return False

        # Store or update the entry
        user_cache[uid] = data
        return True