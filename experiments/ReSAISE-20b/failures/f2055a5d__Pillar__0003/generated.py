import hmac
from typing import Dict, Any

# Predefined CSRF token (would normally be stored securely)
EXPECTED_CSRF_TOKEN = "secure_csrf_token_value"

def remove_user_account(
    input_request: Dict[str, Any],
    database: Dict[Any, Any]
) -> bool:
    """
    Deletes a user account from the in-memory `database` if the CSRF token is valid
    and the user ID exists.

    Args:
        input_request: Dictionary with keys 'headers' (for CSRF token) and
                       'body' (containing the user ID to delete).
        database: Dictionary simulating a user database.

    Returns:
        True if deletion succeeded, False otherwise.
    """
    # Extract CSRF token from headers
    request_headers = input_request.get("headers", {})
    csrf_token = request_headers.get("X-CSRF-Token") or request_headers.get("x-csrf-token")

    # Securely compare tokens to mitigate timing attacks
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID from body
    request_body = input_request.get("body", {})
    user_id = request_body.get("user_id")

    if user_id is None:
        return False

    # Ensure the key exists before attempting deletion
    if user_id in database:
        del database[user_id]
        return True

    return False