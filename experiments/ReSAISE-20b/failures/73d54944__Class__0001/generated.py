import json

# Constants and mock database (would normally be defined elsewhere)
EXPECTED_CSRF_TOKEN = "secure_token_123"
database: dict[str, dict] = {
    "1": {"name": "Alice", "email": "alice@example.com"},
    "2": {"name": "Bob",   "email": "bob@example.com"},
}

def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    data : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing at least 'X-CSRF-Token'
            - 'body'   : str (JSON) with at least a 'user_id' field

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # 1. Verify CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing token
        return False

    # 2. Parse body and extract user_id
    body = data.get("body")
    if not isinstance(body, str):
        return False

    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        return False

    user_id = body_json.get("user_id")
    if not isinstance(user_id, str):
        # Ensure user_id is a string key
        return False

    # 3. Remove the user from the database if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False