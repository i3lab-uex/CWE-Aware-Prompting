import hmac
from typing import Dict, Any

# Simulated global data store and CSRF token (would normally be managed by the framework)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def remove_account(request: Dict[str, Any]) -> bool:
    """
    Remove a user account identified by the `user_id` in the request body.

    Parameters
    ----------
    request : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing request headers.
            - 'body': dict containing the payload, must include 'user_id' and 'csrf_token'.

    Returns
    -------
    bool
        True if the account was successfully deleted, False otherwise.
    """
    # Validate request structure
    try:
        headers = request["headers"]
        body = request["body"]
        user_id = body["user_id"]
        csrf_token = body["csrf_token"]
    except (KeyError, TypeError):
        # Missing required fields
        return False

    # Ensure CSRF token matches using constant‑time comparison to mitigate timing attacks
    if not isinstance(csrf_token, str) or not hmac.compare_digest(csrf_token, EXPECTED_CSRF_TOKEN):
        return False

    # Ensure user_id is a string (or can be cast to one) and exists in the database
    if not isinstance(user_id, str):
        try:
            user_id = str(user_id)
        except Exception:
            return False

    # Perform deletion in a way that avoids race conditions
    try:
        # Acquire lock if database is shared across threads/processes (omitted here for brevity)
        return database.pop(user_id, None) is not None
    except Exception:
        # Any unexpected error should result in a failure return value
        return False