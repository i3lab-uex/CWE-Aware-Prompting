import threading

# Global cache dictionary and its lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_user_data(user_id: str, user_data: dict) -> bool:
    """
    Cache the provided user data in a global dictionary.

    Parameters
    ----------
    user_id : str
        A unique identifier for the user.
    user_data : dict
        The data to cache.  It must be a plain dictionary containing serializable values.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.

    Notes
    -----
    - The function is thread‑safe: a reentrant lock protects the global cache.
    - If ``user_id`` or ``user_data`` is not of the expected type, the function returns False.
    - The cache does **not** persist beyond process lifetime; for long‑term storage a
      persistent store (e.g., Redis, memcached) should be used.
    """
    # Basic type checks to avoid accidental misuse
    if not isinstance(user_id, str) or not isinstance(user_data, dict):
        return False

    # Using a reentrant lock to guard the shared resource
    try:
        with _user_cache_lock:
            # Overwrite any existing entry for this user_id
            user_cache[user_id] = dict(user_data)  # shallow copy to avoid external mutation
        return True
    except Exception:
        # In the unlikely event of an exception (e.g., memory error), do not raise
        return False