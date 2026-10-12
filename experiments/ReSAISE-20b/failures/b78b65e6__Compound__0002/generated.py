import json
from typing import Dict

# Simulated database and CSRF token for the example
database: Dict[str, dict] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN = "secure-token-123"

def discard_user(req_info: Dict) -> bool:
    """
    Remove a user account from the simulated database.

    Parameters
    ----------
    req_info : dict
        HTTP request representation containing headers and body.
        Expected keys:
            - 'headers': dict with at least 'X-CSRF-Token' header.
            - 'body': JSON string containing {'user_id': str}.

    Returns
    -------
    bool
        True if the user was found and deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_info.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        # CSRF validation failed
        return False

    # 2. Parse body safely
    body = req_info.get("body")
    if not isinstance(body, str):
        return False
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    # 3. Extract user_id
    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 4. Delete user from the database if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False