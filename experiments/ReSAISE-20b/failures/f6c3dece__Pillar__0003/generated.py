import threading

# Global in‑memory cache for user data.
user_cache: dict[str, dict] = {}
# A lock to ensure thread‑safe access to the cache.
_cache_lock = threading.RLock()

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store the provided client data in the global `user_cache`.

    Args:
        client_id: A unique string identifier for each user.
        client_data: A dictionary containing various details about the user.

    Returns:
        True if the data was successfully cached, False otherwise.
    """
    # Basic validation to avoid corrupting the cache with invalid keys or data.
    if not isinstance(client_id, str) or not client_id:
        return False
    if not isinstance(client_data, dict):
        return False

    try:
        with _cache_lock:
            # Replace any existing entry for this client_id.
            user_cache[client_id] = client_data.copy()
        return True
    except Exception:
        # Any unexpected error (unlikely with a dict) results in failure.
        return False