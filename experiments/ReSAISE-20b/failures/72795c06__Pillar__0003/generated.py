import threading

# Global cache dictionary for user profiles.
user_cache = {}
# Lock to ensure thread‑safe access to the cache.
_user_cache_lock = threading.RLock()

def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store the given user profile data in an in‑memory cache.

    Args:
        profile_id (str): Unique identifier for the user.
        profile_data (dict): Dictionary containing user details.

    Returns:
        bool: True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid corrupting the cache with invalid inputs
    if not isinstance(profile_id, str) or not isinstance(profile_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Replace any existing entry for the same profile_id
            user_cache[profile_id] = profile_data.copy()
        return True
    except Exception:
        # Any exception (e.g., memory error) is swallowed to satisfy the
        # "no raise" requirement, but we return False to signal failure.
        return False