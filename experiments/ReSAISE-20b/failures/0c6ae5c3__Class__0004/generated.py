import json
from typing import Dict, Any

# Simulated in‑memory database of users
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

# Predefined CSRF token
EXPECTED_CSRF_TOKEN = "secure_token_123"

def erase_user_account(request_info: Dict[str, Any]) -> bool:
    """
    Delete a user account identified by the ID in the request body.

    Parameters
    ----------
    request_info : dict
        Dictionary with keys:
            * headers: mapping containing 'X-CSRF-Token'
            * body   : JSON string or dict with key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. CSRF token validation
    headers = request_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if not csrf_token or csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from body
    body = request_info.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False
    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Verify user exists
    if user_id not in database:
        return False

    # 4. Delete the user
    try:
        del database[user_id]
    except Exception:
        return False

    # 5. Success
    return True