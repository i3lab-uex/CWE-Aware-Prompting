import hmac
from typing import Dict, Any

# Predefined CSRF token for the application
EXPECTED_CSRF_TOKEN = "s3cUrE_T0k3n"

def terminate_user_account(
    request_data: Dict[str, Any],
    database: Dict[Any, Any]
) -> bool:
    """
    Deletes a user account from the in-memory database after validating
    CSRF protection and request payload.

    Parameters
    ----------
    request_data : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': a dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body': a dict containing the user identifier under key 'user_id'

    database : dict
        In-memory dictionary simulating a user database. Keys are user IDs.

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

    # Retrieve and verify CSRF token using constant‑time comparison
    csrf_token = headers.get("X-CSRF-Token")
    if not isinstance(csrf_token, str):
        return False
    if not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Extract user ID and ensure it exists in the database
    user_id = body.get("user_id")
    if user_id is None:
        return False

    # Accept only hashable types for dictionary keys
    if not isinstance(user_id, (int, str)):
        return False

    # Delete the user account if present
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False