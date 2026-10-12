import json
from typing import Dict, Any

# Simulated data store and CSRF token (would normally be defined elsewhere)
database: Dict[str, Any] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-123"

def remove_account(request: Dict[str, Any]) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    request : dict
        HTTP request representation containing:
            - headers: dict with 'X-CSRF-Token'
            - body: str (JSON) containing 'user_id'

    Returns
    -------
    bool
        True if the account was removed, False otherwise.
    """
    # 1. CSRF protection
    headers = request.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF token mismatch or missing
        return False

    # 2. Parse body for user ID
    body = request.get("body", "")
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        # Invalid JSON or body not a string
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, str) or not user_id:
        # Missing or malformed user ID
        return False

    # 3. Attempt to delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False