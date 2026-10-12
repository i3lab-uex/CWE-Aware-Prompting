import threading

# Global cache dictionary and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to mitigate CWE‑400
_MAX_CACHE_ENTRIES = 10_000


def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user-specific information in a global cache.

    Args:
        client_id: Unique identifier for the user.
        info_data: Dictionary containing arbitrary user data.

    Returns:
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(info_data, dict):
        return False

    # Prevent uncontrolled resource consumption by capping cache size
    with _user_cache_lock:
        if len(user_cache) >= _MAX_CACHE_ENTRIES and client_id not in user_cache:
            # Cache is full and the entry to add is new; reject
            return False

        # Store or update the cache entry
        user_cache[client_id] = info_data.copy()  # shallow copy to avoid accidental mutation

    return True