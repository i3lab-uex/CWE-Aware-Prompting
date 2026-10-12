import threading

# Global cache dictionary and its lock for thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to avoid uncontrolled resource consumption.
_MAX_CACHE_SIZE = 10_000

def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for a user.
    cust_data : dict
        Dictionary containing user-related information.

    Returns
    -------
    bool
        True if the entry was stored successfully, False otherwise.
    """
    # Basic validation to avoid storing invalid data
    if not isinstance(cust_id, str) or not cust_id:
        return False
    if not isinstance(cust_data, dict):
        return False

    with _user_cache_lock:
        # Evict an arbitrary entry if cache exceeds maximum size.
        if len(user_cache) >= _MAX_CACHE_SIZE:
            # Simple FIFO eviction: remove an arbitrary key
            try:
                evict_key = next(iter(user_cache))
                del user_cache[evict_key]
            except StopIteration:
                # Cache is empty – nothing to evict
                pass

        try:
            user_cache[cust_id] = cust_data.copy()
            return True
        except Exception:
            # Catch unexpected errors (e.g., memory error) and signal failure
            return False