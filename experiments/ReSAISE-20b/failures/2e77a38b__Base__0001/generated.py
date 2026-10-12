import threading
from collections import OrderedDict

# Global cache and lock for thread‑safety
user_cache: "OrderedDict[str, dict]" = OrderedDict()
cache_lock = threading.Lock()

# Maximum number of entries allowed in the cache to mitigate CWE‑770
MAX_CACHE_SIZE = 1000

def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store or update a customer entry in the global user_cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing arbitrary customer data.

    Returns
    -------
    bool
        True if the entry was added or updated successfully.
        False if the cache is full and the operation cannot proceed
        (the caller may decide to evict or skip).
    """
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    with cache_lock:
        # If the entry already exists, move it to the end (most recent)
        if cust_id in user_cache:
            user_cache.pop(cust_id)

        # Enforce cache size limit
        if len(user_cache) >= MAX_CACHE_SIZE:
            return False

        user_cache[cust_id] = cust_data
    return True