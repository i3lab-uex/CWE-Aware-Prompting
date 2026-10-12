import sys
import threading
from typing import Dict

# Global cache dictionary and associated lock for thread safety
user_cache: Dict[str, dict] = {}
cache_lock = threading.Lock()

# Configuration limits (adjust as needed)
MAX_CACHE_ENTRIES: int = 1_000          # Maximum number of cached users
MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024  # Roughly 50 MB total cache size

def _current_cache_size() -> int:
    """Return the current approximate memory footprint of the cache."""
    size = 0
    for uid, data in user_cache.items():
        # Estimate size of key + value
        size += sys.getsizeof(uid) + sys.getsizeof(data)
    return size

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise (e.g., size or count limits exceeded).

    Notes
    -----
    - The function is thread‑safe.
    - It does not raise exceptions; failures are indicated via the return value.
    """
    if not isinstance(uid, str) or not isinstance(data, dict):
        # Invalid input types; treat as failure
        return False

    with cache_lock:
        # Enforce entry count limit
        if uid not in user_cache and len(user_cache) >= MAX_CACHE_ENTRIES:
            return False

        # Estimate new cache size
        current_size = _current_cache_size()
        added_size = sys.getsizeof(uid) + sys.getsizeof(data)
        if current_size + added_size > MAX_CACHE_SIZE_BYTES:
            return False

        # Store the data
        user_cache[uid] = data
    return True