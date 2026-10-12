import json

# Constants and mock database for demonstration purposes
EXPECTED_CSRF_TOKEN = "secure-token-123"
database: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

def remove_user_data(data: dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    data : dict
        Representation of an HTTP request. Expected keys:
            - "headers": dict, may contain 'X-CSRF-Token'
            - "body": str, JSON containing a field 'user_id'

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

    # Parse the request body
    try:
        body = json.loads(data.get("body", "{}"))
        user_id = int(body["user_id"])
    except (json.JSONDecodeError, KeyError, ValueError):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False