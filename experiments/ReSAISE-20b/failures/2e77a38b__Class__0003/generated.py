import threading
import sys

# Global cache dictionary and its lock for thread safety
user_cache: dict[str, dict] = {}
cache_lock = threading.Lock()

# Maximum allowed number of cached entries to prevent uncontrolled memory growth
MAX_CACHE_SIZE: int = 10_000

# Maximum allowed size (in bytes) for a single cust_data dictionary
MAX_CUST_DATA_SIZE: int = 1_048_576  # 1 MB


def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in a global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing customer data.

    Returns
    -------
    bool
        True if the entry was stored successfully, False otherwise.
    """
    # Basic type validation
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    # Prevent excessive memory usage per entry
    if sys.getsizeof(cust_data) > MAX_CUST_DATA_SIZE:
        return False

    with cache_lock:
        # If the cache is full, refuse new entries
        if len(user_cache) >= MAX_CACHE_SIZE:
            return False

        # Store the data
        user_cache[cust_id] = cust_data.copy()  # copy to avoid external mutation

    return True