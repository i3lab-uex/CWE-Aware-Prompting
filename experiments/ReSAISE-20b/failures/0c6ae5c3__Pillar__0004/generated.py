import json

# Expected CSRF token (should be stored securely in production)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def erase_user_account(request_info: dict, database: dict) -> bool:
    """
    Deletes a user account from an in-memory `database` dictionary.

    Parameters
    ----------
    request_info : dict
        Dictionary containing HTTP request data. Expected keys:
            - 'headers': dict, must contain a 'CSRF-Token' key.
            - 'body': str or dict. If str, JSON-decoded into a dictionary.
    database : dict
        In-memory user database. Keys are user IDs; values are user records.

    Returns
    -------
    bool
        True if the account was found and removed, False otherwise.
    """
    # 1. Validate CSRF token
    headers = request_info.get("headers", {})
    csrf_token = headers.get("CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token: deny deletion
        return False

    # 2. Extract user ID from body
    body = request_info.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id = body_data.get("user_id")
    if not isinstance(user_id, (int, str)):
        return False

    # 3. Delete user from database if present
    try:
        del database[user_id]
        return True
    except KeyError:
        # User ID not found in the database
        return False