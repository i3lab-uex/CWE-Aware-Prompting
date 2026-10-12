import json

# Mock in‑memory user database
database = {
    1: {"name": "Alice"},
    2: {"name": "Bob"},
    3: {"name": "Charlie"}
}

# Expected CSRF token
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

def remove_user_account(req: dict) -> bool:
    """
    Removes a user account identified by `user_id` from the in‑memory database.

    Parameters
    ----------
    req : dict
        Representation of an HTTP request containing:
            - 'headers': a dict with header names and values
            - 'body'   : a JSON string containing the key `user_id`

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # 1. Verify CSRF token
    try:
        csrf_token = req["headers"].get("X-CSRF-Token")
    except (AttributeError, KeyError):
        # Missing headers or token
        return False

    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – possible CSRF attack
        return False

    # 2. Parse body to extract user_id
    try:
        body = req.get("body", "")
        data = json.loads(body)
        user_id = int(data["user_id"])
    except (json.JSONDecodeError, KeyError, ValueError):
        # Malformed body or missing/invalid user_id
        return False

    # 3. Delete the user record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False