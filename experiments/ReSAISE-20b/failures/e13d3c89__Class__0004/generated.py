import json
from typing import Dict, Any

# Simulated database and CSRF token for the example.
database: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"}
}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

def terminate_user_account(request_data: Dict[str, Any]) -> bool:
    """
    Delete a user account from the in-memory database.

    Parameters
    ----------
    request_data : dict
        Dictionary with keys:
            - 'headers': mapping of header names to values, must contain 'X-CSRF-Token'.
            - 'body': raw JSON string containing a key 'user_id'.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # 1. Verify CSRF token
    headers = request_data.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Parse body and validate user_id
    try:
        body = request_data.get("body", "{}")
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, int):
        return False

    # 3. Perform deletion
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False