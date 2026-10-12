import hmac
from typing import Dict, Any

# Predefined CSRF token for the application (in a real app this would be stored securely)
EXPECTED_CSRF_TOKEN: str = "super-secret-csrf-token"

def terminate_user_account(request_data: Dict[str, Any], database: Dict[int, Dict]) -> bool:
    """
    Deletes a user account from the in-memory database after verifying the CSRF token.

    Args:
        request_data: A dictionary representing an HTTP request.
            Expected keys:
                - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
                - 'body': dict containing a numeric 'user_id' key
        database: The in-memory user database keyed by integer user IDs.

    Returns:
        True if the account was successfully deleted, False otherwise.
    """
    # Validate presence of headers and body
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get('headers', {})
    body = request_data.get('body', {})

    # CSRF protection: use constant‑time comparison
    token = headers.get('X-CSRF-Token')
    if not token or not hmac.compare_digest(token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID and ensure it is an integer
    try:
        user_id = int(body.get('user_id'))
    except (TypeError, ValueError):
        return False

    # Perform deletion if the user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False