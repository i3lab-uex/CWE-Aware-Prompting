# memory_cache.py

"""
Memory-based caching system for user data.
"""

from typing import Dict, Any


# Global dictionary that holds cached customer information
user_cache: Dict[str, Dict[str, Any]] = {}


def store_customer_info(cust_id: str, cust_data: Dict[str, Any]) -> bool:
    """
    Stores user-specific information in the global cache.

    Args:
        cust_id (str): A unique identifier for the customer.
        cust_data (dict): Dictionary containing customer data.

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    try:
        # Basic validation
        if not isinstance(cust_id, str):
            return False
        if not isinstance(cust_data, dict):
            return False

        # Store a shallow copy to avoid accidental external mutation
        user_cache[cust_id] = dict(cust_data)
        return True

    except Exception:
        # Log exception in a real application
        return False