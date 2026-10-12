import typing as t

# Constants and mock database (would normally be provided by the surrounding application)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"
database: t.Dict[str, dict] = {}


def remove_user_data(data: t.Dict[str, t.Any]) -> bool:
    """
    Remove a user account from the in-memory database.

    Parameters
    ----------
    data : dict
        A representation of an HTTP request. Expected keys:
            - 'headers': dict containing request headers.
            - 'body': dict containing the payload. Must include a 'user_id' key.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # 1. Extract headers and body safely
    headers: t.Dict[str, str] = data.get("headers", {})
    body: t.Dict[str, t.Any] = data.get("body", {})

    # 2. Verify CSRF token
    csrf_token: str = headers.get("X-CSRF-Token", "")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – potential CSRF or unauthorized request
        return False

    # 3. Validate presence of user_id in body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 4. Attempt to delete the user record
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False