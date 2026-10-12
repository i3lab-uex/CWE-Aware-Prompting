import threading

# Global cache dictionary for storing customer data.
user_cache: dict[str, dict] = {}
# A lock to ensure thread‑safe updates to the cache.
_cache_lock = threading.RLock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store user-specific data in the global `user_cache`.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing arbitrary customer data.

    Returns
    -------
    bool
        True if the entry was stored successfully, False otherwise.
    """
    # Basic validation: ensure identifiers are non‑empty strings and data is a dict
    if not isinstance(cust_id, str) or not cust_id.strip():
        return False
    if not isinstance(cust_data, dict):
        return False

    try:
        with _cache_lock:
            # Overwrite any existing entry for the same cust_id.
            user_cache[cust_id] = dict(cust_data)  # shallow copy to avoid external mutation
        return True
    except Exception:
        # In case of any unexpected error, do not crash; simply return False.
        return False