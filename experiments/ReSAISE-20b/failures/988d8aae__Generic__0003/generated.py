import sys
import threading

# Global cache and configuration limits
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

# Configuration constants
MAX_ENTRIES = 10_000                # maximum number of cached users
MAX_TOTAL_SIZE_BYTES = 10 * 1024**2  # maximum total size (~10 MiB)

def _current_cache_size() -> int:
    """Return the approximate size in bytes of all cached client data."""
    total = 0
    for value in user_cache.values():
        # Rough size estimation: recursively sum sizes of nested objects
        total += sys.getsizeof(value)
    return total

def cache_client_info(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific details in the global cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for a user.
    client_data : dict
        Dictionary containing user attributes.

    Returns
    -------
    bool
        True if the entry was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(client_id, str) or not isinstance(client_data, dict):
        return False

    with _user_cache_lock:
        # Reject if cache would exceed entry limit
        if len(user_cache) >= MAX_ENTRIES and client_id not in user_cache:
            return False

        # Estimate new size if we add/replace this entry
        current_size = _current_cache_size()
        # Subtract size of existing entry if present
        old_entry_size = sys.getsizeof(user_cache[client_id]) if client_id in user_cache else 0
        new_entry_size = sys.getsizeof(client_data)
        projected_size = current_size - old_entry_size + new_entry_size

        if projected_size > MAX_TOTAL_SIZE_BYTES:
            return False

        # Store a shallow copy to avoid accidental external mutation
        user_cache[client_id] = client_data.copy()
    return True