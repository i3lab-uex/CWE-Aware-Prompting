import threading

# Global cache dictionary and its lock for thread‑safe access
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

def cache_application_data(client_id: str, info_data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    client_id : str
        A unique identifier for the user.
    info_data : dict
        Dictionary containing user-related information to be cached.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation (avoid raising exceptions)
    if not isinstance(client_id, str) or not isinstance(info_data, dict):
        return False

    # Optionally enforce a maximum size for the cache (e.g., 10,000 entries)
    MAX_CACHE_SIZE = 10000
    with _user_cache_lock:
        if len(user_cache) >= MAX_CACHE_SIZE and client_id not in user_cache:
            # Cache is full and we're adding a new entry – reject to avoid unbounded growth
            return False

        # Store a shallow copy to prevent accidental external mutation
        user_cache[client_id] = dict(info_data)

    return True