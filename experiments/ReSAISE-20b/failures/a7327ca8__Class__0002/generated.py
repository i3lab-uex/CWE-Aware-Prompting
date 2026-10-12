import json

# Simulated global data store and CSRF token
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "securetoken123"

def remove_account(request: dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    request : dict
        The HTTP request representation. Expected keys:
            - 'headers': a mapping of header names to values.
            - 'body': a JSON string or dict containing the user ID.

    Returns
    -------
    bool
        True if the account was deleted successfully, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF verification failed
        return False

    # 2. Extract user ID from the request body
    raw_body = request.get("body")
    if raw_body is None:
        return False

    # Body may be a dict or JSON string
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
        # User ID must be an integer
        return False

    # 3. Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User does not exist
    return False