import json

# Predefined CSRF token used by the application
EXPECTED_CSRF_TOKEN = "secure-csrf-token-12345"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` after validating
    the CSRF token and ensuring the user ID exists.

    Parameters:
        input_request (dict): HTTP request representation containing
            - 'headers': dict with key 'X-CSRF-Token'
            - 'body': JSON string or dict containing 'user_id'
        database (dict): In-memory user database keyed by user ID.

    Returns:
        bool: True if the account was successfully removed, False otherwise.
    """
    # 1. CSRF token validation
    headers = input_request.get("headers", {})
    token = headers.get("X-CSRF-Token")
    if token != EXPECTED_CSRF_TOKEN:
        # Invalid or missing CSRF token
        return False

    # 2. Extract user ID from request body
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
    if user_id is None:
        return False

    # 3. Ensure the user ID exists in the database
    if user_id not in database:
        return False

    # 4. Delete the user entry
    try:
        del database[user_id]
    except Exception:
        # In a real system we might log this error
        return False

    return True