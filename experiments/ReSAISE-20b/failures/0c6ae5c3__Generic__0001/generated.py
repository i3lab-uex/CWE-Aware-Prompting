import json
from typing import Dict

# Predefined CSRF token for validation
EXPECTED_CSRF_TOKEN = "secure-csrf-token-123"

# Simulated in‑memory user database
database: Dict[str, dict] = {
    "user1": {"name": "Alice", "email": "alice@example.com"},
    "user2": {"name": "Bob",   "email": "bob@example.com"},
}

def erase_user_account(request_info: Dict) -> bool:
    """
    Deletes a user account from the in‑memory database.

    Parameters
    ----------
    request_info : dict
        Dictionary representing an HTTP request. Expected keys:
            - 'headers': dict containing the CSRF token under key 'X-CSRF-Token'
            - 'body'   : JSON string or dict containing the key 'user_id'

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Validate request structure
    headers = request_info.get("headers")
    body = request_info.get("body")

    if not isinstance(headers, dict) or not isinstance(body, (dict, str)):
        return False

    # 2. CSRF token check
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 3. Parse body (handle both dict and JSON string)
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False

    if not isinstance(body, dict):
        return False

    user_id = body.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 4. Delete user from database if exists
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False