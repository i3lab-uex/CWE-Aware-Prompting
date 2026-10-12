import hmac
from typing import Dict

# Simulated database and CSRF token (normally provided by the surrounding application)
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "s3cr3t_csrf_token"

def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account based on the request information.

    Parameters
    ----------
    req_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - "headers": mapping of header names to values.
              Must contain "X-CSRF-Token".
            - "body": mapping that contains a key "user_id" with the ID to delete.

    Returns
    -------
    bool
        True if the user was found and removed; False otherwise.
    """
    # 1. Validate CSRF token using constant‑time comparison
    headers = req_info.get("headers", {})
    incoming_token = headers.get("X-CSRF-Token")
    if not incoming_token:
        return False

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 2. Extract user ID from request body
    body = req_info.get("body", {})
    user_id = body.get("user_id")
    if not user_id:
        return False

    # 3. Attempt to delete the user from the database
    try:
        del database[user_id]
        return True
    except KeyError:
        # User ID not present in the database
        return False