import json

# Mock database: user_id -> user data
database = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}

# Expected CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_profile(request_data: dict) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A dictionary representing an HTTP request. It must contain:
            - 'headers': a dict of request headers
            - 'body'   : a JSON string or dict with the key 'user_id'

    Returns
    -------
    bool
        True if the user was removed successfully, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # Validate request structure
    if not isinstance(request_data, dict):
        raise ValueError("request_data must be a dictionary")

    headers = request_data.get("headers")
    body   = request_data.get("body")

    if headers is None or body is None:
        raise ValueError("Missing 'headers' or 'body' in request_data")

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # Invalid CSRF token

    # Parse body (handle both dict and JSON string)
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            raise ValueError("Body is not valid JSON")

    if not isinstance(body, dict):
        raise ValueError("Body must be a dictionary after parsing")

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        raise ValueError("'user_id' must be a string")

    # Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False