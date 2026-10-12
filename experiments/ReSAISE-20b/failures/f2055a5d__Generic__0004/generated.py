import hmac

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` if the CSRF token is valid
    and the requested user ID exists.

    Parameters:
        input_request (dict): HTTP request representation containing
            - 'headers': dict with a 'X-CSRF-Token' key
            - 'body': dict containing the 'user_id' to delete
        database (dict): In-memory user database mapping user IDs to user data

    Returns:
        bool: True if the account was successfully deleted, False otherwise.
    """
    # Validate presence of required sections
    headers = input_request.get("headers")
    body = input_request.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # Retrieve and validate CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve user ID to delete
    user_id = body.get("user_id")
    if not isinstance(user_id, (str, int)):
        return False

    # Attempt deletion
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # Catch unexpected errors (e.g., read-only dict)
            return False

    # User ID not found
    return False