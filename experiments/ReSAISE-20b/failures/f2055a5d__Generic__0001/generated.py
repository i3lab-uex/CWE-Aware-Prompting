import typing

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def remove_user_account(
    input_request: typing.Dict[str, typing.Any],
    database: typing.Dict[int, dict]
) -> bool:
    """
    Deletes a user account from the in-memory database.

    Parameters
    ----------
    input_request : dict
        HTTP request dictionary containing:
            - 'headers': mapping of header names to values (expects 'X-CSRF-Token')
            - 'body': mapping containing 'user_id' key
    database : dict[int, dict]
        In-memory user database mapping user IDs to user data.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Validate CSRF token
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Validate body and user_id
    body = input_request.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False