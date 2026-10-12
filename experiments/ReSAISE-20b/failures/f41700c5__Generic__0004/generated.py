# memory based user cache implementation

from copy import deepcopy
from typing import Dict, Any

# Global dictionary that holds cached user data
user_cache: Dict[str, Dict[str, Any]] = {}


def store_user_info(identifier: str, data_info: Dict[str, Any]) -> bool:
    """
    Stores user-specific information in the global `user_cache` dictionary.

    Args:
        identifier (str): A unique string that identifies each user.
        data_info (dict): A dictionary containing various user-related information.

    Returns:
        bool: True if the data was cached successfully, False otherwise.
    """
    # Basic validation
    if not isinstance(identifier, str) or not identifier:
        return False

    if not isinstance(data_info, dict):
        return False

    try:
        # Store a deep copy to prevent accidental external modifications
        user_cache[identifier] = deepcopy(data_info)
        return True
    except Exception:
        # In a real-world scenario, log the exception here
        return False