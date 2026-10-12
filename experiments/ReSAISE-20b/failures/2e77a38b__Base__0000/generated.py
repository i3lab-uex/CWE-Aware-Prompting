# memory_cache.py

from threading import RLock
from typing import Dict, Any

# Global cache dictionary and its lock for thread‑safety
user_cache: Dict[str, Dict[str, Any]] = {}
_cache_lock = RLock()

# Maximum number of entries allowed in the cache (CWE‑770 mitigation)
_MAX_CACHE_SIZE = 10_000

def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Store customer data in an in‑memory cache.

    Args:
        cust_id: Unique identifier for the customer.
        cust_data: Dictionary containing customer‑specific data.

    Returns:
        True if the entry was added/updated successfully,
        False if the cache has reached its maximum size.
    """
    # Basic validation
    if not isinstance(cust_id, str) or not isinstance(cust_data, dict):
        return False

    with _cache_lock:
        # Enforce maximum cache size
        if cust_id not in user_cache and len(user_cache) >= _MAX_CACHE_SIZE:
            # Cache is full; reject new entries
            return False

        # Store or update the customer data
        user_cache[cust_id] = cust_data.copy()  # copy to avoid external mutation

    return True