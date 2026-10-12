import hmac

# Constants and mock database (to be provided by the surrounding system)
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    # ... other user records
}

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing:
            - headers: a dict with at least the 'X-CSRF-Token' key.
            - body: a dict that must contain a numeric 'user_id'.

    Returns
    -------
    bool
        True if the user was found and removed; False otherwise.
    """
    # 1. Validate CSRF token using constant-time comparison
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract and validate user_id
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Perform deletion if user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False