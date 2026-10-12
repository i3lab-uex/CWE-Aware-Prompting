import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to avoid uncontrolled growth
_MAX_CACHE_SIZE = 10_000


def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store user profile data in an in‑memory cache.

    Args:
        profile_id: Unique string identifier for the user.
        profile_data: Dictionary containing user details.

    Returns:
        True if caching succeeded, False otherwise (e.g., cache full).
    """
    if not isinstance(profile_id, str) or not isinstance(profile_data, dict):
        return False

    with _user_cache_lock:
        # Enforce cache size limit
        if len(user_cache) >= _MAX_CACHE_SIZE and profile_id not in user_cache:
            # Cache full and this is a new entry – refuse to cache
            return False

        user_cache[profile_id] = profile_data.copy()  # store a shallow copy
    return True