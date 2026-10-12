import re

# Constants and mock database (for illustration purposes)
EXPECTED_CSRF_TOKEN = "s3cureT0ken123"
database: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account identified by `user_id` in the request body.
    
    Parameters
    ----------
    req : dict
        A representation of an HTTP request. It must contain a header key
        'X-CSRF-Token' and a body key 'user_id'.
    
    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    
    Raises
    ------
    ValueError
        If required data is missing or malformed.
    """
    # 1. Verify CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Do not reveal whether the token was wrong; just fail silently
        return False

    # 2. Extract and validate user_id
    body = req.get("body", {})
    user_id_raw = body.get("user_id")
    if not isinstance(user_id_raw, (int, str)):
        return False

    # Ensure user_id is an integer and positive
    try:
        user_id = int(user_id_raw)
        if user_id <= 0:
            return False
    except (ValueError, TypeError):
        return False

    # 3. Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False