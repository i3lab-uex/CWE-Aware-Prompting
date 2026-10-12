import hmac

# Simulated data store and CSRF token (normally these would be configured elsewhere)
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_token_123"

def discard_user(req_info: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_info : dict
        Dictionary representing an HTTP request. Expected to contain:
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body':   dict with a 'user_id' key.

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.
    """
    # Basic validation of request structure
    headers = req_info.get("headers", {})
    body   = req_info.get("body", {})

    # Retrieve and validate CSRF token using constant-time comparison
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token or not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID and ensure it is an integer
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False