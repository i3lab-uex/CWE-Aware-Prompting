import hmac

# Predefined CSRF token (in a real application this would be stored securely)
EXPECTED_CSRF_TOKEN = "super_secret_csrf_token"

def remove_user_account(input_request: dict, database: dict) -> bool:
    """
    Delete a user account from an in-memory database after verifying CSRF token
    and ensuring the provided user ID is valid.

    Args:
        input_request (dict): HTTP request representation with 'headers' and 'body'.
        database (dict): In-memory user database mapping user IDs to user data.

    Returns:
        bool: True if deletion succeeded, False otherwise.
    """
    # Extract CSRF token from headers
    csrf_token = input_request.get("headers", {}).get("X-CSRF-Token")
    if not csrf_token:
        return False

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID from body and validate type
    try:
        user_id = input_request.get("body", {}).get("user_id")
        if not isinstance(user_id, int):
            return False
    except Exception:
        return False

    # Attempt to delete the user entry safely
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # Unexpected deletion error (e.g., database corruption)
            return False

    # User not found
    return False