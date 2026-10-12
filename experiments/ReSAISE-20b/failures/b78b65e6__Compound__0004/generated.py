import json

# Simulated database and CSRF token constant (in real code these would come from a secure source)
database = {
    "user1": {"name": "Alice"},
    "user2": {"name": "Bob"},
}
EXPECTED_CSRF_TOKEN = "secure-token-12345"

def discard_user(req_info: dict) -> bool:
    """
    Delete a user account from the simulated database.

    Parameters
    ----------
    req_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict of HTTP headers (case-insensitive)
            - 'body'  : JSON string or dict containing the user ID under key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.

    Notes
    -----
    * CSRF protection: the request must include a header 'X-CSRF-Token' that matches
      EXPECTED_CSRF_TOKEN.
    * The user ID is extracted from the request body. If missing or not present in
      the database, deletion fails.
    """
    # 1. CSRF token validation
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID from body
    body = req_info.get("body")
    if body is None:
        return False

    # Body may be a dict or a JSON string
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id = body_data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False