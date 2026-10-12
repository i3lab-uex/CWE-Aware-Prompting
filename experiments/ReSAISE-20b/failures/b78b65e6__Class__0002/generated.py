import hmac
from typing import Dict, Any

# Simulated database of users: {user_id: user_data}
database: Dict[int, Any] = {}

# Expected CSRF token (normally stored securely)
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def discard_user(req_info: Dict[str, Any]) -> bool:
    """
    Deletes a user account identified by `user_id` in the request body.

    Parameters
    ----------
    req_info : dict
        Dictionary containing HTTP request data. Expected keys:
            - "headers": mapping of header names to values
            - "body": mapping that includes 'user_id' and optionally 'csrf_token'

    Returns
    -------
    bool
        True if the user was deleted successfully, False otherwise.
    """
    # 1. Extract headers and body
    headers = req_info.get("headers", {})
    body = req_info.get("body", {})

    # 2. CSRF token validation (use constant‑time comparison)
    incoming_token = body.get("csrf_token") or headers.get("X-CSRF-Token")
    if not incoming_token:
        return False
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Validate and sanitize user_id
    raw_user_id = body.get("user_id")
    try:
        user_id = int(raw_user_id)
    except (TypeError, ValueError):
        return False

    # 4. Ensure user exists
    if user_id not in database:
        return False

    # 5. Delete the user
    try:
        del database[user_id]
    except Exception:
        return False

    # 6. Success
    return True