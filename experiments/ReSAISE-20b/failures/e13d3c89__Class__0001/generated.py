import json
from typing import Dict

# Predefined CSRF token used by the application (normally stored securely)
EXPECTED_CSRF_TOKEN = "super-secret-csrf-token"

# In-memory user database simulation
database: Dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... other users
}


def terminate_user_account(request_data: Dict) -> bool:
    """
    Delete a user account based on the request data.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request with the following keys:
            - 'headers': dict, must contain a valid CSRF token under key 'X-CSRF-Token'
            - 'body': dict, must contain the integer user ID under key 'user_id'

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Basic structure validation
    if not isinstance(request_data, dict):
        return False

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF token verification
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # Ensure the user exists before attempting deletion
    if user_id not in database:
        return False

    # Perform the deletion
    try:
        del database[user_id]
    except Exception:
        return False

    return True