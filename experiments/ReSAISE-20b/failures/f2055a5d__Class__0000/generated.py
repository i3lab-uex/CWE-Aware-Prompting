import json

# Predefined CSRF token for verification
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` if the request
    contains a valid CSRF token and a legitimate user ID.

    Parameters:
        input_request (dict): HTTP request representation with
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : JSON string or dict containing a numeric 'user_id'

        database (dict): In-memory user database mapping user IDs to user data.

    Returns:
        bool: True if the account was deleted, False otherwise.
    """
    # 1. CSRF token validation
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str) or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract and validate user ID from body
    body = input_request.get("body")
    if isinstance(body, str):
        try:
            body_data = json.loads(body)
        except json.JSONDecodeError:
            return False
    elif isinstance(body, dict):
        body_data = body
    else:
        return False

    user_id = body_data.get("user_id")
    if not isinstance(user_id, int) or user_id <= 0:
        return False

    # 3. Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False