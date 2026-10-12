import json

# Expected CSRF token used to validate incoming requests
EXPECTED_CSRF_TOKEN = "your-secure-csrf-token"

def discard_user(req_info: dict, database: dict) -> bool:
    """
    Delete a user account from the simulated `database` based on an HTTP request.

    Parameters
    ----------
    req_info : dict
        Dictionary representing the HTTP request. Expected keys:
            - 'headers': dict of request headers.
            - 'body'   : str or bytes containing JSON with a `user_id` field.
    database : dict
        Simulated data store mapping user IDs to user information.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    body = req_info.get("body")
    if not body:
        return False

    try:
        # Body may be bytes or str; ensure it's a string
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        data = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete user from database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False