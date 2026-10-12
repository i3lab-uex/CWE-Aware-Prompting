import threading

# Global cache dictionary and its lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def cache_profile_data(profile_id: str, profile_data: dict) -> bool:
    """
    Store the given profile data in the global user_cache.

    Args:
        profile_id: A unique string identifier for each user.
        profile_data: Dictionary containing user details.

    Returns:
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid accidental overwrites or invalid data
    if not isinstance(profile_id, str) or not profile_id:
        return False

    if not isinstance(profile_data, dict):
        return False

    try:
        # Use a lock to ensure atomic update of the shared cache
        with _user_cache_lock:
            # Prevent accidental modification by storing a shallow copy
            user_cache[profile_id] = dict(profile_data)
        return True
    except Exception:
        # In case of any unexpected error, do not raise; simply signal failure
        return False