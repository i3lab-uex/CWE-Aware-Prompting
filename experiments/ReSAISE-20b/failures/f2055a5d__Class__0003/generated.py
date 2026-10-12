import hmac

# Expected CSRF token (predefined for the application)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_123"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Deletes a user account from the in-memory `database` after verifying
    the CSRF token and that the request contains a valid user ID.

    Parameters:
        input_request (dict): HTTP-like request containing 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body": {"user_id": "<id>"}
                }
        database (dict): Dictionary mapping user IDs to user data.

    Returns:
        bool: True if the account was deleted, False otherwise.
    """
    # Validate presence of headers and body
    if not isinstance(input_request, dict):
        return False

    headers = input_request.get("headers", {})
    body = input_request.get("body", {})

    # Secure CSRF token comparison using hmac.compare_digest
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID from body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Attempt to delete the user
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User not found
            return False
    except Exception:
        # Any unexpected error results in a safe failure
        return False