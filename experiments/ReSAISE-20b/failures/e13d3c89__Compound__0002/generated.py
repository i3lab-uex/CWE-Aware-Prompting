import hmac

# Constants (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure_expected_token"

def terminate_user_account(request_data: dict, database: dict) -> bool:
    """
    Delete a user account from an in-memory database after verifying the CSRF token.

    Parameters
    ----------
    request_data : dict
        Dictionary with keys 'headers' (mapping of header names to values) and
        'body' (a mapping containing the user ID under key 'user_id').
    database : dict
        In-memory dictionary simulating a user database. Keys are user IDs,
        values are user records.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if not csrf_token:
        return False

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Validate body and user ID
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, TypeError, ValueError):
        return False

    # 3. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False