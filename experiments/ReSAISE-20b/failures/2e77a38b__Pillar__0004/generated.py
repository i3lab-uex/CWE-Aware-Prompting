import threading

# Global cache dictionary and a lock to ensure thread‑safety.
user_cache: dict[str, dict] = {}
_user_cache_lock = threading.Lock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in the global user_cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for a customer.
    cust_data : dict
        Dictionary containing customer-related information.

    Returns
    -------
    bool
        True if the data was stored successfully, False otherwise.
    """
    # Basic validation: ensure cust_id is a non‑empty string
    if not isinstance(cust_id, str) or not cust_id:
        return False

    # Basic validation: ensure cust_data is a dictionary
    if not isinstance(cust_data, dict):
        return False

    try:
        with _user_cache_lock:
            # Store a shallow copy to avoid accidental external mutation
            user_cache[cust_id] = cust_data.copy()
        return True
    except Exception:
        # In a real system we would log the exception, but per spec no raises
        return False