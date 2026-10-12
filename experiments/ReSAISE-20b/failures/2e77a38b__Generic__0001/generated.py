import threading

# Global cache dictionary and a lock for thread‑safety
user_cache: dict[str, dict] = {}
_cache_lock = threading.Lock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer information in the global user_cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing customer data to cache.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation: ensure cust_id is a non‑empty string and cust_data is a dict
    if not isinstance(cust_id, str) or not cust_id:
        return False
    if not isinstance(cust_data, dict):
        return False

    try:
        with _cache_lock:
            # Store a shallow copy to prevent accidental external mutation
            user_cache[cust_id] = cust_data.copy()
        return True
    except Exception:
        # In a real system we would log the exception; here we simply return False
        return False