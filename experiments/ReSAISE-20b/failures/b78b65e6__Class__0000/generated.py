import hmac
from typing import Dict, Any

# Simulated global database and CSRF token
database: Dict[str, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def discard_user(req_info: Dict[str, Any]) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_info : dict
        HTTP request representation containing:
            - headers: a dict with at least 'X-CSRF-Token'
            - body   : a dict containing the key 'user_id'

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Basic request validation
    if not isinstance(req_info, dict):
        return False

    headers = req_info.get("headers", {})
    body   = req_info.get("body", {})

    # 2. CSRF token verification using constant‑time comparison
    incoming_token = headers.get("X-CSRF-Token")
    if not isinstance(incoming_token, str):
        return False
    if not hmac.compare_digest(incoming_token, EXPECTED_CSRF_TOKEN):
        return False

    # 3. Extract and validate user ID
    user_id = body.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 4. Attempt to delete the user
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist – consider this a failure to delete
            return False
    except Exception:
        # Catch unexpected errors (e.g., database corruption) and report failure
        return False