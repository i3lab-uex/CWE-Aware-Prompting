import threading

# Global in‑memory cache for user account data.
user_cache: dict[str, dict] = {}
# A lock to protect concurrent access to the cache.
_cache_lock = threading.RLock()


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    account_id : str
        A unique identifier for the user. Must be a non‑empty string.
    account_data : dict
        A dictionary containing the user's information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``.

    Notes
    -----
    * The function is thread‑safe; concurrent calls will not corrupt the cache.
    * No external resources are held, so the function cannot leak file handles or network
      sockets.  It only manipulates Python objects in memory.
    * The function performs minimal validation to avoid obvious misuse (e.g. empty
      identifiers or non‑dict payloads).  All other errors are caught and cause a
      graceful failure (returning ``False``) rather than raising an exception.
    """
    if not isinstance(account_id, str) or not account_id:
        return False
    if not isinstance(account_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to prevent accidental mutation by callers.
            user_cache[account_id] = dict(account_data)
        return True
    except Exception:
        # Catch all exceptions to avoid leaking internal state or resource handles.
        return False