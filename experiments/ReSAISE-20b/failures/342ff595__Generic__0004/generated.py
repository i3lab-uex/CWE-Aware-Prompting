import uuid
from typing import Dict, Any

# Mock in‑memory database: keys are user IDs (UUID strings), values are user data dicts
database: Dict[str, Dict[str, Any]] = {}

# Expected CSRF token for the request
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"


def remove_user_profile(request_data: Dict[str, Any]) -> bool:
    """
    Remove a user profile from the mock database.

    Parameters
    ----------
    request_data : dict
        A representation of an HTTP request containing headers and body.
        Expected keys:
            - "headers": dict, must contain a 'X-CSRF-Token' header.
            - "body": dict, must contain a 'user_id' key with the UUID string.

    Returns
    -------
    bool
        True if the user was successfully removed, False otherwise.
    """
    # Validate request structure
    headers = request_data.get("headers")
    body = request_data.get("body")

    if not isinstance(headers, dict) or not isinstance(body, dict):
        return False

    # CSRF protection
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # Validate that the user ID is a valid UUID (optional but adds safety)
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