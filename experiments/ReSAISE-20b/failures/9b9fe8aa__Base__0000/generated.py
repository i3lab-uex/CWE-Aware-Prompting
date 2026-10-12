import sys
import threading
from typing import Dict

# Global cache dictionary and associated lock for thread safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits to mitigate CWE‑770
MAX_CACHE_ENTRIES: int = 10_000          # maximum number of cached users
MAX_TOTAL_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024   # ~50 MiB

def _current_cache_size() -> int:
    """Return the approximate memory footprint of the entire cache."""
    size = 0
    for key, value in user_cache.items():
        # Rough estimation: sizes of keys + values
        size += sys.getsizeof(key) + sys.getsizeof(value)
    return size

def cache_user_info(user_identifier: str, user_details: dict) -> bool:
    """
    Store `user_details` in the global cache under `user_identifier`.

    The function enforces limits on both the number of entries and the total
    memory consumption to prevent uncontrolled growth (CWE‑770).

    Parameters
    ----------
    user_identifier : str
        A unique identifier for the user.
    user_details : dict
        User-specific attributes and details.

    Returns
    -------
    bool
        True if the entry was added successfully; False otherwise.
    """
    # Basic validation
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    with _user_cache_lock:
        # If the user is already cached, update in place
        if user_identifier in user_cache:
            user_cache[user_identifier] = user_details
            return True

        # Enforce entry count limit
        if len(user_cache) >= MAX_CACHE_ENTRIES:
            return False

        # Estimate the size of the new entry
        entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)

        # Enforce total size limit
        if _current_cache_size() + entry_size > MAX_TOTAL_CACHE_SIZE_BYTES:
            return False

        # Insert the new entry
        user_cache[user_identifier] = user_details
        return True