import secrets

# Predefined CSRF token (should be kept secret in real applications)
EXPECTED_CSRF_TOKEN = "secure_random_token_value"

def terminate_user_account(request_data: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` if the CSRF token is valid
    and the provided user ID exists.

    Parameters:
        request_data (dict): HTTP request representation containing
            - 'headers': dict with a 'X-CSRF-Token' key.
            - 'body': dict with a 'user_id' key.
        database (dict): In-memory user store mapping user IDs to user data.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # Basic request structure validation
    try:
        headers = request_data["headers"]
        body = request_data["body"]
    except (KeyError, TypeError):
        return False

    # Validate CSRF token using a constant-time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not secrets.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Validate user ID
    user_id = body.get("user_id")
    if user_id is None:
        return False
    # Accept both int and str representations of an ID, but normalise to str for dict key
    if isinstance(user_id, int):
        user_key = str(user_id)
    elif isinstance(user_id, str) and user_id.isdigit():
        user_key = user_id
    else:
        return False

    # Perform deletion if the user exists
    if user_key in database:
        del database[user_key]
        return True

    # User not found
    return False