import collections

# Global cache dictionary with a maximum size to avoid unbounded memory growth.
MAX_CACHE_SIZE = 10_000          # Adjust as needed for your application.
_user_cache: collections.OrderedDict[str, dict] = collections.OrderedDict()


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in a memory‑based cache.

    Parameters
    ----------
    cust_id : str
        A unique identifier for the customer.
    cust_data : dict
        Customer related information to cache.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    # Basic validation to avoid storing meaningless entries
    if not isinstance(cust_id, str) or not cust_id:
        return False
    if not isinstance(cust_data, dict):
        return False

    # Evict the oldest entry if we have reached maximum capacity
    if len(_user_cache) >= MAX_CACHE_SIZE:
        # popitem(last=False) removes the first (oldest) item
        _user_cache.popitem(last=False)

    # Insert or update the cache entry, moving it to the end as most recently used
    _user_cache[cust_id] = cust_data
    _user_cache.move_to_end(cust_id)

    return True


# Optional helper: retrieve cached data (not part of the required API)
def get_customer_info(cust_id: str):
    """Return cached data for a given customer ID, or None if not found."""
    return _user_cache.get(cust_id)