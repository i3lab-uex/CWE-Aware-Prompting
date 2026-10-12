import uuid
from typing import Dict, Any

# Mock database: user_id (str) -> user data (dict)
database: Dict[str, Dict[str, Any]] = {}

# Expected CSRF token constant
EXPECTED_CSRF_TOKEN: str = "s3cr3t_csrf_token"

def remove_user_profile(request_data: Dict[str, Any]) -> bool:
    """
    Remove a user profile from the in-memory database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing:
            - 'headers': dict with at least the 'X-CSRF-Token' header
            - 'body': dict containing a key 'user_id'

    Returns
    -------
    bool
        True if the account was removed successfully, False otherwise.

    Raises
    ------
    ValueError
        If the request format is invalid or missing required fields.
    """

    # Validate structure of request_data
    if not isinstance(request_data, dict):
        raise ValueError("request_data must be a dictionary")

    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        raise ValueError("headers and body must be dictionaries")

    # CSRF protection: check token
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False  # CSRF check failed

    # Retrieve user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Ensure the user ID is a valid UUID string
    try:
        uuid_obj = uuid.UUID(user_id, version=4)
    except (ValueError, AttributeError):
        return False

    # Attempt to delete the user record
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False