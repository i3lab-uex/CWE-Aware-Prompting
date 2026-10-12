import hmac

# Predefined CSRF token used by the application.
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def terminate_user_account(request_data: dict, database: dict) -> bool:
    """
    Deletes a user account from an in-memory database after verifying CSRF token.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' key.
            - 'body': dict containing a 'user_id' key (int or str).
    database : dict
        In-memory dictionary mapping user IDs to user information.

    Returns
    -------
    bool
        True if the account was found and deleted, False otherwise.
    """
    # Ensure required structure
    headers = request_data.get("headers", {})
    body = request_data.get("body", {})

    # Retrieve CSRF token from headers
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token is None:
        return False

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve user ID from request body
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Attempt to delete the user
    try:
        del database[user_id]
        return True
    except KeyError:
        # User does not exist
        return False