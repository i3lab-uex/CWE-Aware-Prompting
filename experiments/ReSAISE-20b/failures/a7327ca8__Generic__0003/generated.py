import json

# Constants and simulated database (for demonstration purposes)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"
database: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}


def remove_account(request: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    request : dict
        An HTTP request representation containing:
            - 'headers': a mapping of header names to values.
            - 'body':   the raw request body (JSON string or dict).

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.

    Notes
    -----
    - The CSRF token must be present in the request headers under
      'X-CSRF-Token' and match EXPECTED_CSRF_TOKEN.
    - The user ID must be supplied in the request body under the key
      'user_id' and be an integer that exists in the database.
    - No exception is raised; all error conditions return False.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    raw_body = request.get("body")
    if raw_body is None:
        return False

    # Body can be a dict or JSON string
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except (json.JSONDecodeError, TypeError):
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Delete user from database if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False