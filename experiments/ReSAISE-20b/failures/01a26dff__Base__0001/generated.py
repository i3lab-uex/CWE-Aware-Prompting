# Cache module for user account information

from typing import Dict

# Global cache dictionary
user_cache: Dict[str, dict] = {}

# Maximum allowed entries in the cache to mitigate CWE-770
MAX_CACHE_SIZE: int = 10_000

def cache_account_info(account_id: str, account_data: dict) -> bool:
    """
    Stores user-specific data in an in-memory cache.

    Args:
        account_id (str): Unique identifier for the user.
        account_data (dict): Dictionary containing user details.

    Returns:
        bool: True if caching succeeds, False otherwise.
    """
    # Validate input types
    if not isinstance(account_id, str) or not isinstance(account_data, dict):
        return False

    # Enforce cache size limit
    if len(user_cache) >= MAX_CACHE_SIZE:
        return False

    # Store the data
    try:
        user_cache[account_id] = account_data.copy()
        return True
    except Exception:
        # In the unlikely event of a failure, do not raise
        return False