# cache_user_info.py

"""
A lightweight, memory‑based caching module for user data.
The cache is a simple global dictionary (`user_cache`) that stores
user details keyed by a unique user identifier.
The module enforces two limits:
  * A maximum total memory footprint (bytes) for the cache.
  * A maximum number of cached entries.

If adding a new entry would exceed either limit, the function
returns False and does not modify the cache.
"""

import sys
from typing import Dict, Any

# Global cache dictionary
user_cache: Dict[str, Dict[str, Any]] = {}

# Configuration constants (adjustable)
_MAX_CACHE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
_MAX_CACHE_ENTRIES: int = 1_000


def _current_cache_size() -> int:
    """Return the current memory size of the cache in bytes."""
    total = 0
    for key, value in user_cache.items():
        total += sys.getsizeof(key) + sys.getsizeof(value)
    return total


def cache_user_info(user_identifier: str, user_details: Dict[str, Any]) -> bool:
    """
    Store a user's details in the global cache.

    Parameters
    ----------
    user_identifier : str
        Unique identifier for the user (e.g., username, email, UUID).
    user_details : dict
        Dictionary containing arbitrary user attributes.

    Returns
    -------
    bool
        True if the entry was added successfully, False if adding it would exceed
        either the size or count limits.

    Notes
    -----
    * The function is intentionally tolerant: it never raises an exception.
      It simply returns False on failure, allowing the caller to handle the
      situation gracefully (e.g., fallback to a database query).
    * The cache is not thread‑safe. If used in a multi‑threaded environment,
      wrap accesses with a lock.
    """
    # Ensure the identifier is a string
    if not isinstance(user_identifier, str):
        return False

    # Ensure the details are a dictionary
    if not isinstance(user_details, dict):
        return False

    # Compute prospective size increase
    new_entry_size = sys.getsizeof(user_identifier) + sys.getsizeof(user_details)

    # Check entry count limit
    if len(user_cache) >= _MAX_CACHE_ENTRIES and user_identifier not in user_cache:
        return False

    # Check memory size limit
    current_size = _current_cache_size()
    if current_size + new_entry_size > _MAX_CACHE_SIZE_BYTES and user_identifier not in user_cache:
        return False

    # Store or update the entry
    user_cache[user_identifier] = user_details
    return True


# Example usage (uncomment for quick test)
if __name__ == "__main__":
    # Populate cache with dummy data
    for i in range(5):
        uid = f"user_{i}"
        details = {"name": f"User {i}", "age": 20 + i}
        success = cache_user_info(uid, details)
        print(f"Caching {uid}: {'Success' if success else 'Failed'}")

    # Inspect cache size
    print(f"Cache contains {len(user_cache)} entries, size: {_current_cache_size()} bytes")