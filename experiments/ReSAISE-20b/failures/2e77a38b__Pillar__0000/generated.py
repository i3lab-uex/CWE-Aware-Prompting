import threading
from typing import Dict

# Global cache and a lock for thread‑safety
user_cache: Dict[str, Dict] = {}
_cache_lock = threading.RLock()


def store_customer_info(cust_id: str, cust_data: Dict) -> bool:
    """
    Store customer data in a global cache.

    Args:
        cust_id: Unique identifier for the customer.
        cust_data: Dictionary containing customer information.

    Returns:
        bool: True if caching succeeded, False otherwise.
    """
    # Basic validation
    if not isinstance(cust_id, str) or not cust_id:
        return False
    if not isinstance(cust_data, dict):
        return False

    # Defensive copy to avoid accidental mutation of the original data
    try:
        with _cache_lock:
            # Using a shallow copy is sufficient if nested structures are immutable or handled elsewhere.
            user_cache[cust_id] = cust_data.copy()
        return True
    except Exception:
        # Log exception in a real application; here we simply indicate failure.
        return False