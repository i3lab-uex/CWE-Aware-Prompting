import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to mitigate CWE‑770
_MAX_CACHE_SIZE = 10_000

def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    identifier : str
        Unique string identifying a user.
    data_info : dict
        Dictionary containing the user's information.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic type validation to avoid accidental misuse
    if not isinstance(identifier, str) or not isinstance(data_info, dict):
        return False

    with _user_cache_lock:
        # Enforce cache size limit to prevent resource exhaustion
        if len(user_cache) >= _MAX_CACHE_SIZE and identifier not in user_cache:
            return False

        # Store or update the entry
        user_cache[identifier] = data_info.copy()  # copy to avoid external mutation

    return True