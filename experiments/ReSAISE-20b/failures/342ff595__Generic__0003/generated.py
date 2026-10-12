import json

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"
database = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory `database`.

    Parameters
    ----------
    request_data : dict
        A dictionary representing an HTTP request with the following keys:
            - "headers": dict, must contain "X-CSRF-Token"
            - "body":   str or dict, JSON string or parsed body containing the key "user_id"

    Returns
    -------
    bool
        True if the user was found and removed, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id from the body
    body = request_data.get("body")
    if body is None:
        return False

    # Body may be a JSON string or already parsed dict
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Delete the user record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False