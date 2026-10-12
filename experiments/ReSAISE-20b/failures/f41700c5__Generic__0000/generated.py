# memory_based_cache.py

"""
Memory-based caching system for user data.

This module provides a simple in-memory cache to store and retrieve
user-specific information, reducing the need for repeated database queries.
"""

# Global cache dictionary
user_cache: dict[str, dict] = {}

def store_user_info(identifier: str, data_info: dict) -> bool:
    """
    Store user-specific information in the global cache.

    Args:
        identifier (str): A unique string that identifies each user.
        data_info (dict): Dictionary containing various user-related information.

    Returns:
        bool: True if caching succeeded, False otherwise.
    """
    try:
        # Basic validation
        if not isinstance(identifier, str) or not identifier:
            return False
        if not isinstance(data_info, dict):
            return False

        # Store a shallow copy to avoid accidental external mutations
        user_cache[identifier] = data_info.copy()
        return True
    except Exception:
        # Swallow all exceptions to comply with "Raise: None"
        return False