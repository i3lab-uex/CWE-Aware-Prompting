import json

# Mock in-memory database: user_id -> user_record
database = {}

# Expected CSRF token constant (in real code this would be securely stored)
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"


def remove_user_account(req: dict) -> bool:
    """
    Remove a user account identified by `user_id` in the request body.

    Parameters
    ----------
    req : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': mapping of header names to values.
            - 'body': JSON string containing at least a 'user_id' field.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Parse request body safely
    try:
        body = json.loads(req.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract user_id; it must be a non-empty string
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        return False

    # 4. Delete the user record if it exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False