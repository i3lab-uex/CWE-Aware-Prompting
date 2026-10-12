import threading

# Global cache dictionary and a lock to guard concurrent access
user_cache: dict[str, dict] = {}
_cache_lock = threading.RLock()

# Optional cache size limit to mitigate memory exhaustion (CWE-664 concern)
_MAX_CACHE_SIZE = 10_000  # Adjust as appropriate for the application

def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store user-specific data in the global `user_cache`.

    Parameters
    ----------
    cust_id : str
        A unique identifier for the customer.
    cust_data : dict
        Arbitrary data associated with the customer.

    Returns
    -------
    bool
        True if the entry was stored successfully, False otherwise.
    """
    # Basic validation to avoid storing malformed data
    if not isinstance(cust_id, str) or not cust_id:
        return False

    if not isinstance(cust_data, dict):
        return False

    try:
        with _cache_lock:
            # If cache is at capacity, evict the oldest entry (simple LRU policy)
            if len(user_cache) >= _MAX_CACHE_SIZE:
                # Remove an arbitrary item; for a real LRU, use OrderedDict or collections.deque
                user_cache.pop(next(iter(user_cache)))

            # Store the new entry
            user_cache[cust_id] = cust_data.copy()  # shallow copy to avoid external mutation

        return True
    except Exception:
        # Silently handle unexpected errors to satisfy the "Raise: None" requirement
        return False