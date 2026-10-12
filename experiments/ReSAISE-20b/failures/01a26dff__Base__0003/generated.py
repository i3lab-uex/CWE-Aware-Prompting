import threading

# Global cache dictionary and lock for thread‑safety
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Configuration: maximum number of cached entries to mitigate CWE‑770
_MAX_CACHE_SIZE = 10_000  # Adjust as appropriate for your environment


def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Store user-specific data in an in‑memory cache.

    Parameters
    ----------
    account_id : str
        A unique string identifier for each user.
    account_data : dict
        Dictionary containing various details about the user.

    Returns
    -------
    bool
        True if caching succeeds, False if it fails (e.g., cache limit reached).

    Notes
    -----
    - Thread‑safe via a lock.
    - Enforces a maximum cache size to prevent uncontrolled memory growth
      (CWE‑770 mitigation).
    - Does not perform deep copy; caller should avoid mutating the supplied
      dictionary after caching if isolation is required.
    """
    # Basic validation to avoid storing invalid keys
    if not isinstance(account_id, str) or not account_id:
        return False

    # Ensure account_data is a dictionary
    if not isinstance(account_data, dict):
        return False

    with _user_cache_lock:
        # Enforce cache size limit
        if len(user_cache) >= _MAX_CACHE_SIZE and account_id not in user_cache:
            # Cache is full and this key is new → reject to avoid unlimited growth
            return False

        # Store (or overwrite) the entry
        user_cache[account_id] = account_data

    return True