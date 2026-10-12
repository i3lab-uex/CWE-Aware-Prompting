import hmac

# Simulated database and expected CSRF token (normally stored securely)
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def delete_user_account(request: dict) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    request : dict
        A dictionary representing an HTTP request. It must contain:
            - 'headers': a dict with the header keys.
              The CSRF token should be in the 'X-CSRF-Token' header.
            - 'body': a dict containing at least the key 'user_id'.
              The value must be an integer representing the user to delete.

    Returns
    -------
    bool
        True if the deletion succeeded, False otherwise.
    """
    # 1. Validate request structure
    try:
        headers = request["headers"]
        body   = request["body"]
    except (KeyError, TypeError):
        # Malformed request
        return False

    # 2. CSRF protection (constant‑time comparison to avoid timing attacks)
    csrf_token = headers.get("X-CSRF-Token", "")
    if not isinstance(csrf_token, str):
        return False
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    try:
        user_id = body["user_id"]
    except KeyError:
        return False
    if not isinstance(user_id, int):
        return False

    # 4. Delete the user if present
    try:
        del database[user_id]
    except KeyError:
        # User does not exist
        return False

    return True