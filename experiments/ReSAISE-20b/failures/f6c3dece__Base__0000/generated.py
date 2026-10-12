import threading

# Global cache and configuration
user_cache: dict[str, dict] = {}
CACHE_LOCK = threading.Lock()
MAX_CACHE_SIZE = 10_000          # Limit the number of cached entries to avoid unbounded growth
MAX_CLIENT_DATA_SIZE = 1_048_576  # 1 MB per entry as an example limit

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store client data in an in‑memory cache.

    Parameters
    ----------
    client_id : str
        Unique identifier for the user.
    client_data : dict
        Dictionary containing user details.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation of arguments
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    # Enforce per‑entry size limit (to mitigate memory exhaustion)
    try:
        entry_size = len(str(client_data).encode('utf-8'))
    except Exception:
        return False
    if entry_size > MAX_CLIENT_DATA_SIZE:
        return False

    with CACHE_LOCK:
        # Enforce overall cache size limit
        if len(user_cache) >= MAX_CACHE_SIZE and client_id not in user_cache:
            return False
        # Store or update the entry
        user_cache[client_id] = client_data.copy()
    return True