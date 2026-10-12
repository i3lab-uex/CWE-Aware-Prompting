import threading

# Global cache dictionary and a lock for thread‑safe access
user_cache: dict[str, dict] = {}
cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to mitigate CWE‑400
MAX_CACHE_SIZE = 10_000


def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user data in an in‑memory cache.

    Args:
        client_id (str): Unique identifier for the user.
        client_data (dict): Dictionary containing user details.

    Returns:
        bool: True if the data was cached successfully, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    with cache_lock:
        # Prevent uncontrolled growth of the cache
        if len(user_cache) >= MAX_CACHE_SIZE:
            return False

        # Store a shallow copy to avoid accidental external modifications
        user_cache[client_id] = client_data.copy()
    return True