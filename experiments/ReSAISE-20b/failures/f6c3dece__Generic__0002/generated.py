# Global cache dictionary for user data
user_cache: dict[str, dict] = {}

def cache_client_data(client_id: str, client_data: dict) -> bool:
    """
    Store user-specific data in an in-memory cache.

    Args:
        client_id (str): A unique identifier for the user.
        client_data (dict): User details to cache.

    Returns:
        bool: True if the data was cached successfully, False otherwise.
    """
    try:
        # Ensure client_id is a string and client_data is a dict
        if not isinstance(client_id, str) or not isinstance(client_data, dict):
            return False

        # Store a shallow copy to prevent accidental external modifications
        user_cache[client_id] = client_data.copy()
        return True
    except Exception:
        # Any unexpected error results in a failure flag
        return False