import json

# Simulated database and CSRF token constant
database = {}  # user_id (str) -> user_data (dict)
EXPECTED_CSRF_TOKEN = "expected_csrf_token_value"


def remove_account(request: dict) -> bool:
    """
    Remove a user account from the simulated database.

    Args:
        request (dict): HTTP request representation. Expected to contain:
            - headers: dict with key 'X-CSRF-Token' or similar.
            - body: JSON string or dict containing the user ID under key 'user_id'.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch: potential CSRF attack
        return False

    # 2. Extract user ID from body
    raw_body = request.get("body")
    if isinstance(raw_body, str):
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            return False
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False