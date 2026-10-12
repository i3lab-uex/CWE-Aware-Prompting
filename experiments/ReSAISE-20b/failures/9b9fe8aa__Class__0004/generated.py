import sys
from typing import Dict

# Global cache dictionary
user_cache: Dict[str, Dict] = {}

# Configuration limits for the cache (adjust as needed)
MAX_CACHE_COUNT: int = 10_000          # Maximum number of cached users
MAX_CACHE_SIZE_BYTES: int = 50 * 1024 * 1024  # Maximum total size (≈50 MiB)

def _current_cache_size() -> int:
    """
    Estimate the current memory footprint of `user_cache` in bytes.
    Uses sys.getsizeof on each key and value, plus a small overhead per entry.
    """
    size = 0
    for key, value in user_cache.items():
        size += sys.getsizeof(key)
        size += sys.getsizeof(value)
    return size

def cache_user_info(user_identifier: str, user_details: Dict) -> bool:
    """
    Store `user_details` in the global `user_cache` under the key
    `user_identifier`.  The operation succeeds only if adding this entry
    does not exceed the configured cache limits.

    Parameters:
        user_identifier (str): Unique identifier for the user.
        user_details (dict): Dictionary containing user attributes.

    Returns:
        bool: True if the entry was cached successfully, False otherwise.
    """
    global user_cache

    # Validate input types
    if not isinstance(user_identifier, str) or not isinstance(user_details, dict):
        return False

    # If the user is already cached, replace it without size check
    if user_identifier in user_cache:
        user_cache[user_identifier] = user_details
        return True

    # Preliminary size estimation for the new entry
    entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)

    # Check count limit
    if len(user_cache) >= MAX_CACHE_COUNT:
        return False

    # Check size limit
    if _current_cache_size() + entry_size > MAX_CACHE_SIZE_BYTES:
        return False

    # Store the new entry
    user_cache[user_identifier] = user_details
    return True