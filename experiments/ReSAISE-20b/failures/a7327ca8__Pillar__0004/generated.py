import re
from typing import Dict

# Simulated data store and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN = "secure_token_12345"

def remove_account(request: Dict) -> bool:
    """
    Delete a user account from the database.

    Parameters
    ----------
    request : dict
        HTTP request representation containing:
            - headers: dict, may contain 'X-CSRF-Token'
            - body: dict, must include 'user_id'

    Returns
    -------
    bool
        True if the user account was successfully deleted,
        False otherwise.

    Raises
    ------
    ValueError
        If the request structure is invalid or required fields are missing.
    """
    # Validate request structure
    if not isinstance(request, dict):
        raise ValueError("Request must be a dictionary.")

    headers = request.get("headers", {})
    body = request.get("body", {})

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("Headers and body must be dictionaries.")

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Do not reveal whether the token was missing or wrong
        return False

    # Extract and validate user_id
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Basic sanitization: allow only alphanumerics and underscores
    if not re.fullmatch(r"[A-Za-z0-9_]+", user_id):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False