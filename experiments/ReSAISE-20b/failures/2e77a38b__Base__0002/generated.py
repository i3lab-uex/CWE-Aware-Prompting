import threading
from collections import OrderedDict

# Global cache with a fixed maximum size to mitigate CWE-770
_MAX_CACHE_SIZE = 1000

# OrderedDict preserves insertion order, enabling LRU eviction.
_user_cache: OrderedDict[str, dict] = OrderedDict()
_cache_lock = threading.Lock()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in a memory cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing customer-related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation: ensure identifiers and data are hashable / serializable
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    with _cache_lock:
        # Evict least-recently-used item if cache exceeds capacity
        if cust_id not in _user_cache and len(_user_cache) >= _MAX_CACHE_SIZE:
            # Remove the oldest item (first key)
            _user_cache.popitem(last=False)

        # Store or update the entry
        _user_cache[cust_id] = cust_data

    return True