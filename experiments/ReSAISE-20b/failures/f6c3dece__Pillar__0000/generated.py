import threading

# Global cache dictionary and its lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs to avoid corrupting the cache
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Replace any existing entry for the same client_id
            user_cache[client_id] = dict(client_data)  # shallow copy to avoid external mutation
        return True
    except Exception:
        # Any exception (unlikely with a dict) is swallowed to meet the spec
        return False