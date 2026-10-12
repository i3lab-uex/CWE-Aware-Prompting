import threading

# Global in‑memory cache for client data.
# Using a thread‑safe dictionary with a lock to prevent race conditions.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.RLock()


def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store client data in the global in‑memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if caching succeeded, False otherwise.
    """
    # Basic validation: client_id must be a non‑empty string,
    # and client_data must be a dictionary.
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Overwrite any existing entry; this is intentional to keep
            # the cache up‑to‑date.
            user_cache[client_id] = client_data.copy()
        return True
    except Exception:
        # Swallow any exception and signal failure.
        return False