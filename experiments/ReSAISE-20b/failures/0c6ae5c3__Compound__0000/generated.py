import json
from typing import Dict, Any

# Example global variables (would normally be provided by the application)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_123"
database: Dict[str, Any] = {}  # Simulated user database keyed by user_id


def erase_user_account(request_info: Dict[str, Any]) -> bool:
    """
    Delete a user account from the in-memory `database` if the request is valid.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing a 'X-CSRF-Token' key.
            - 'body': JSON string or dict containing the user ID under the key 'user_id'.

    Returns
    -------
    bool
        True if the account was deleted; False otherwise (e.g., CSRF failure, missing user,
        or invalid input).
    """
    # Validate request structure
    if not isinstance(request_info, dict):
        return False

    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # CSRF token validation
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Parse body (allow either dict or JSON string)
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False