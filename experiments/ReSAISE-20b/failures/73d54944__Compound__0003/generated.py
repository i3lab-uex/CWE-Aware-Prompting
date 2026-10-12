import json

# Expected CSRF token (should be securely stored in real applications)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_data(data: dict, database: dict) -> bool:
    """
    Remove a user account from the in-memory `database` using the provided
    request data. The function verifies a CSRF token to mitigate
    Cross‑Site Request Forgery attacks.

    Parameters:
        data (dict): Representation of an HTTP request. Expected keys:
            - 'headers': dict containing request headers
            - 'body'   : JSON string with at least the key 'user_id'
        database (dict): In‑memory user database keyed by user ID.

    Returns:
        bool: True if the account was removed successfully, False otherwise.
    """
    # 1. Verify CSRF token
    headers = data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch or missing -> potential CSRF
        return False

    # 2. Extract user_id from request body
    body = data.get("body")
    if not body:
        return False

    try:
        payload = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = payload.get("user_id")
    if not user_id:
        return False

    # 3. Remove the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False