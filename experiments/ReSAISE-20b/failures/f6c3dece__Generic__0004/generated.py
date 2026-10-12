import threading

# Global in-memory cache for client data.
user_cache: dict[str, dict] = {}
# A lock to ensure thread‑safe access to the cache.
_cache_lock = threading.RLock()


def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in an in-memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing arbitrary user information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``.

    Notes
    -----
    * The function uses a re‑entrant lock to make cache updates thread safe.
    * It performs minimal validation: ``client_id`` must be a non‑empty string
      and ``client_data`` must be a dictionary.  If validation fails, the
      function returns ``False`` without raising an exception.
    * The cache is purely in‑memory; data will be lost on process exit.
    """
    # Basic validation
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[client_id] = client_data.copy()
        return True
    except Exception:
        # Any unexpected error is swallowed; the caller only gets a boolean.
        return False