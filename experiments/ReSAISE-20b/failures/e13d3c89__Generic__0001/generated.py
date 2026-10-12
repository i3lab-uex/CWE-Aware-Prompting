import typing

# Expected CSRF token for the application
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

def terminate_user_account(
    request_data: typing.Dict[str, typing.Any],
    database: typing.Dict[int, dict]
) -> bool:
    """
    Delete a user account from the in-memory `database`.

    Parameters
    ----------
    request_data : dict
        HTTP request data. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' header.
            - 'body': dict containing the key 'user_id'.
    database : dict
        In‑memory user database mapping user IDs to user info.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid CSRF token – do not proceed
        return False

    # 2. Extract user ID from body
    body = request_data.get("body", {})
    try:
        user_id = int(body["user_id"])
    except (KeyError, TypeError, ValueError):
        # Malformed request
        return False

    # 3. Remove user from database if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False