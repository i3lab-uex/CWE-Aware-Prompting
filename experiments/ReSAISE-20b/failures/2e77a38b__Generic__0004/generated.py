# Global cache dictionary for storing customer data
user_cache: dict[str, dict] = {}

def store_customer_info(cust_id: str, cust_data: dict) -> bool:
    """
    Store customer data in the global user_cache.

    Parameters
    ----------
    cust_id : str
        Unique identifier for the customer.
    cust_data : dict
        Dictionary containing user-related information.

    Returns
    -------
    bool
        True if the data was cached successfully, False otherwise.
    """
    try:
        # Basic validation: ensure cust_id is a non-empty string
        if not isinstance(cust_id, str) or not cust_id:
            return False

        # Ensure cust_data is a dictionary
        if not isinstance(cust_data, dict):
            return False

        # Store the data in the cache
        user_cache[cust_id] = cust_data.copy()  # copy to avoid accidental mutations

        return True
    except Exception:
        # Any unexpected error results in a failure indication
        return False