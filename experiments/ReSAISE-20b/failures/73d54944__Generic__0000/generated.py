import typing as _t

# Expected CSRF token constant
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

def remove_user_data(
    data: _t.Dict[str, _t.Any],
    database: _t.Dict[int, _t.Any]
) -> bool:
    """
    Remove a user from the in-memory database.

    Parameters
    ----------
    data : dict
        HTTP request representation containing:
            - 'headers': mapping of header names to values.
            - 'body'   : mapping containing at least 'user_id'.
    database : dict
        In-memory user database keyed by integer user IDs.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # Validate CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID safely
    body = data.get("body", {})
    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False

    # Ensure the ID is an integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # Remove the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False