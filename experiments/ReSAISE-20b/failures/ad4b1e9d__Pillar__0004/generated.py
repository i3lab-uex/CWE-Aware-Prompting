import json
from typing import Dict, Any

# Simulated database and CSRF token for demonstration purposes
database: Dict[str, Dict[str, Any]] = {}
EXPECTED_CSRF_TOKEN: str = "expected_csrf_token_value"

def erase_user_profile(req_payload: Dict[str, Any]) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload. Expected to contain:
            - 'headers': dict with a 'X-CSRF-Token' key
            - 'body': str or dict that includes the user ID under the key 'user_id'

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.

    Raises
    ------
    ValueError
        If required fields are missing or malformed.
    """
    # 1. Validate CSRF token
    headers = req_payload.get("headers")
    if not isinstance(headers, dict):
        return False
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch
        return False

    # 2. Extract user ID from the request body
    body = req_payload.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Perform the deletion atomically
    try:
        if user_id in database:
            del database[user_id]
            return True
        else:
            # User does not exist; consider this a non‑error scenario
            return False
    except Exception:
        # Catch unforeseen errors (e.g., race conditions) and fail safely
        return False