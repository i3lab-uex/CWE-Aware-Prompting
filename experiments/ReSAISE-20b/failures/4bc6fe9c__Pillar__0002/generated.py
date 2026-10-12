import sys
import threading
from typing import Dict

# Global cache and its lock for thread‑safety
user_cache: Dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration limits (configurable if needed)
_MAX_ENTRIES: int = 10_000          # maximum number of cached users
_MAX_TOTAL_SIZE_BYTES: int = 50 * 1024 * 1024  # ~50 MB total payload

def _current_cache_size() -> int:
    """Return the approximate memory footprint of all cached values."""
    total = 0
    for value in user_cache.values():
        # sys.getsizeof returns the size of the container, not nested objects.
        # For a more accurate estimate we sum sizes recursively but keep it
        # lightweight for this example.
        total += sys.getsizeof(value)
    return total

def store_user_data(uid: str, data: dict) -> bool:
    """
    Store or update user information in the global cache.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise (e.g., size or count limits exceeded).

    Notes
    -----
    - The function is thread‑safe.
    - Existing entries with the same UID are replaced; size accounting accounts for the
      difference between old and new payloads.
    - No exceptions are raised; callers should check the return value.

    Security
    --------
    - The function does not perform any serialization; it stores the dictionary as‑is.
      This limits accidental exposure of sensitive data via string representations.
    - Input validation is minimal; callers should ensure `uid` and `data` meet application
      security policies.
    """
    if not isinstance(uid, str) or not isinstance(data, dict):
        # Basic type check; reject invalid inputs silently
        return False

    with _user_cache_lock:
        # Determine size impact of the new entry
        new_entry_size = sys.getsizeof(data)

        if uid in user_cache:
            # Replace existing entry: adjust size by diff
            old_entry_size = sys.getsizeof(user_cache[uid])
            projected_total = _current_cache_size() - old_entry_size + new_entry_size
        else:
            # New entry: check count and size limits
            if len(user_cache) >= _MAX_ENTRIES:
                return False
            projected_total = _current_cache_size() + new_entry_size

        if projected_total > _MAX_TOTAL_SIZE_BYTES:
            return False

        # Safe to cache
        user_cache[uid] = data.copy()  # shallow copy to avoid accidental external mutation

    return True