import json
from typing import Dict

# Simulated data store and CSRF token for the example
database: Dict[str, dict] = {
    "user_1": {"name": "Alice", "email": "alice@example.com"},
    "user_2": {"name": "Bob",   "email": "bob@example.com"},
}
EXPECTED_CSRF_TOKEN: str = "secure-token-123"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Remove a user account from the system.

    Parameters
    ----------
    req_payload : dict
        A dictionary representing an HTTP request. It should contain:
          - 'headers': a mapping of header names to values.
          - 'body':   the request body as a JSON string.

    Returns
    -------
    bool
        True if the user was successfully deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token") or headers.get("x-csrf-token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user ID from the request body
    try:
        body = req_payload.get("body", "")
        if isinstance(body, bytes):
            body = body.decode()
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return False

    user_id = data.get("user_id")
    if not isinstance(user_id, str):
        return False

    # 3. Delete the user from the database
    if user_id in database:
        del database[user_id]
        return True

    # User not found
    return False