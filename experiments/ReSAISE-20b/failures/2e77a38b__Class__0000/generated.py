# -*- coding: utf-8 -*-
"""
Memory‑based caching system for customer data.

The cache is a simple dictionary that maps a unique customer ID
(`cust_id`) to the corresponding data (`cust_data`).  To avoid
unbounded memory growth (CWE‑400), the cache size is capped at a
configurable maximum.  When the limit would be exceeded, the oldest
entry is evicted (FIFO).  The function returns ``True`` on success
and ``False`` if the input is invalid.
"""

from collections import OrderedDict
from typing import Dict, Any

# Global cache with a maximum size (adjust as needed)
MAX_CACHE_SIZE = 10_000
user_cache: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()


def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Store customer information in the global cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing customer-related information.

    Returns
    -------
    bool
        ``True`` if the data was cached successfully, otherwise ``False``.

    Notes
    -----
    - The function checks that both arguments are of the expected type.
    - If the cache is full, the oldest entry (the first inserted) is removed
      to keep memory usage bounded.
    - The function does not raise exceptions; it returns ``False`` on
      invalid input to keep the API simple for callers.
    """
    # Validate arguments
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    # If the key already exists, update its value and move it to the end
    if cust_id in user_cache:
        user_cache.move_to_end(cust_id)
        user_cache[cust_id] = cust_data
        return True

    # Enforce cache size limit
    if len(user_cache) >= MAX_CACHE_SIZE:
        # Remove the oldest entry (FIFO)
        user_cache.popitem(last=False)

    # Insert new entry
    user_cache[cust_id] = cust_data
    return True