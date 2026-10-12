import hmac

# Example constants and database; in real usage these would be defined elsewhere
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

def erase_user_account(request_info: dict) -> bool:
    """
    Delete a user account based on the provided request information.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was successfully deleted; False otherwise.
    """
    # Validate request structure
    headers = request_info.get("headers", {})
    body   = request_info.get("body", {})

    # CSRF token validation (constant‑time comparison)
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract and validate user ID
    try:
        user_id = int(body.get("user_id"))
    except (TypeError, ValueError):
        return False

    # Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False