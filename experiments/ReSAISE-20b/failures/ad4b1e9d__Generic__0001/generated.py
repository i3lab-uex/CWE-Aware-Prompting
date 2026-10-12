import json

# Simulated constants and data store (for illustration)
EXPECTED_CSRF_TOKEN = "secure_token_123"
database: dict[str, dict] = {
    # Example user entries
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}

def erase_user_profile(req_payload: dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        HTTP request payload containing headers and body. Expected keys:
            - 'headers': dict with a 'X-CSRF-Token' entry.
            - 'body': JSON string or dict containing 'user_id'.

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.
    """
    # 1. CSRF protection
    try:
        headers = req_payload.get("headers", {})
        token = headers.get("X-CSRF-Token")
    except Exception:
        return False

    if token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Extract user ID from body
    try:
        body = req_payload.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete user from database if exists
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User not found
            return False
    except Exception:
        # Any unexpected error during deletion
        return False