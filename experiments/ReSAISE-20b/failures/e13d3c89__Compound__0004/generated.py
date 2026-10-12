import hmac
from typing import Dict, Any

# Constants and simulated database (to be provided by the caller)
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"
database: Dict[str, Any] = {}

def terminate_user_account(request_data: Dict[str, Any]) -> bool:
    """
    Delete a user account identified by `user_id` in the request body after verifying
    the CSRF token present in the request headers.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' key.
            - 'body':   dict containing a 'user_id' key.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Validate request structure
    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # Extract and validate CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID and validate type
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Perform deletion only if the user exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False