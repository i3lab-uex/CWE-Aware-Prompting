import json

# Simulated database and CSRF token
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def erase_user_profile(req_payload: dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected keys:
            - 'headers': dict containing at least the 'X-CSRF-Token' header.
            - 'body':   dict or JSON string containing the user ID under key 'user_id'.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    body = req_payload.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    user_id_raw = body.get("user_id")
    if user_id_raw is None:
        return False

    # 3. Validate that the ID is an integer
    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError):
        return False

    # 4. Delete the user if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False