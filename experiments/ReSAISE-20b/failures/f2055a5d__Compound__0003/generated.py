import hmac
from typing import Dict

# Global constants and simulated database
EXPECTED_CSRF_TOKEN = "secure_csrf_token_12345"
database: Dict[str, dict] = {}


def remove_user_account(input_request: Dict) -> bool:
    """
    Deletes a user account based on the provided request.

    Args:
        input_request (dict): Dictionary containing 'headers' and 'body'.
            Expected structure:
                {
                    "headers": {"X-CSRF-Token": "<token>"},
                    "body":   {"user_id": "<id>"}
                }

    Returns:
        bool: True if deletion succeeded, False otherwise.

    Raises:
        None
    """
    # Validate CSRF token using constant-time comparison
    headers = input_request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID from request body
    body = input_request.get("body", {})
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # Delete the user if present
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False