import re

# Mock database: user_id -> user data dictionary
database = {
    "user123": {"name": "Alice"},
    "user456": {"name": "Bob"},
}

# Expected CSRF token value
EXPECTED_CSRF_TOKEN = "secure_token_123"

def remove_user_account(req: dict) -> bool:
    """
    Remove a user account identified by `user_id` from the in-memory database.

    Parameters
    ----------
    req : dict
        HTTP request representation. Expected keys:
            - "headers": dict containing 'X-CSRF-Token'
            - "body":   dict containing 'user_id'

    Returns
    -------
    bool
        True if the user was removed successfully, False otherwise.
    """
    # 1. CSRF token validation
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token missing or incorrect
        return False

    # 2. Extract and validate user_id from body
    body = req.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", user_id):
        # Invalid or malformed user ID
        return False

    # 3. Attempt to delete the user record
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User ID does not exist
            return False
    except Exception:
        # Any unexpected error results in failure
        return False