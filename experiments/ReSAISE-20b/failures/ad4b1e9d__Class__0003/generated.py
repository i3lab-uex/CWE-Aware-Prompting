import json
from typing import Dict

# Simulated in‑memory data store (user_id -> user_info)
database: Dict[str, dict] = {
    "alice": {"name": "Alice", "role": "user"},
    "bob":   {"name": "Bob",   "role": "admin"},
}

# Expected CSRF token for request validation
EXPECTED_CSRF_TOKEN: str = "secure_csrf_token_12345"

def erase_user_profile(req_payload: Dict) -> bool:
    """
    Deletes a user account from the simulated database.

    Parameters
    ----------
    req_payload : dict
        The HTTP request payload containing:
            - headers: a mapping of header names to values
            - body   : a JSON string or dict with the key 'user_id'

    Returns
    -------
    bool
        True if the user was deleted, False otherwise.
    """
    # 1. Verify CSRF token
    headers = req_payload.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # 2. Extract user_id from body
    body = req_payload.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except (json.JSONDecodeError, TypeError):
            return False
    if not isinstance(body, dict) or "user_id" not in body:
        return False

    user_id = body["user_id"]
    if not isinstance(user_id, str):
        return False

    # 3. Delete the user from the database
    if user_id in database:
        try:
            del database[user_id]
            return True
        except Exception:
            # Any unexpected exception during deletion results in failure
            return False

    # User does not exist
    return False