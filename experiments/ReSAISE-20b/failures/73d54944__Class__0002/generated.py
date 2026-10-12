import hmac
from typing import Dict, Any

# Mock in‑memory user database: {user_id: user_record}
database: Dict[str, Any] = {}

# Expected CSRF token (normally stored securely on the server)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_value"

def remove_user_data(data: Dict[str, Any]) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    data : dict
        A dictionary representing an HTTP request. Expected keys:
            - 'headers': a dict containing the CSRF token under key 'X-CSRF-Token'.
            - 'body': a dict containing the user ID under key 'user_id'.

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.
    """
    # Basic validation of input structure
    if not isinstance(data, dict):
        return False

    headers = data.get("headers", {})
    body   = data.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # Retrieve and verify CSRF token
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Retrieve user ID from the request body
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Attempt to delete the user record
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False