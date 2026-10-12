import json
from typing import Dict

# Simulated global database and CSRF token
database: Dict[str, dict] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

def discard_user(req_info: Dict) -> bool:
    """
    Delete a user account based on the request information.

    Parameters
    ----------
    req_info : dict
        Dictionary containing HTTP request data. Expected keys:
            - 'headers': dict, must include 'X-CSRF-Token'
            - 'body': str or bytes containing JSON with a 'user_id' field

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Validate CSRF token
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # Token mismatch – reject silently
        return False

    # 2. Extract body and parse JSON safely
    body = req_info.get("body")
    if not body:
        return False

    # Accept both str and bytes
    try:
        if isinstance(body, bytes):
            body_str = body.decode("utf-8")
        else:
            body_str = str(body)
    except Exception:
        return False

    try:
        payload = json.loads(body_str)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Validate user_id
    user_id = payload.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        return False

    # 4. Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False