from typing import Dict, Any

# Predefined CSRF token for validation (example value)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def remove_user_account(input_request: Dict[str, Any], database: Dict[int, Any]) -> bool:
    """
    Deletes a user account from an in-memory database after verifying CSRF token and input validity.

    Parameters
    ----------
    input_request : dict
        A dictionary representing an HTTP request. It must contain:
            - 'headers': a mapping that includes the CSRF token under key 'X-CSRF-Token'.
            - 'body': a mapping that includes the user ID under key 'user_id'.

    database : dict
        An in-memory dictionary mapping user IDs (int) to user data.

    Returns
    -------
    bool
        True if the account was found and deleted, False otherwise.
    """
    # 1. Validate presence of required fields
    headers = input_request.get("headers")
    body   = input_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # 2. Verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Extract and validate user_id
    raw_user_id = body.get("user_id")
    if raw_user_id is None:
        return False

    try:
        user_id = int(raw_user_id)
    except (ValueError, TypeError):
        return False

    # 4. Delete user if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False