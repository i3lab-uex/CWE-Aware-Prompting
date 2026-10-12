import json
from typing import Dict

# Mock in‑memory database and CSRF token constant
database: Dict[int, dict] = {}
EXPECTED_CSRF_TOKEN: str = "secure-csrf-token-12345"

def remove_user_account(req: Dict) -> bool:
    """
    Remove a user account from the mock database.

    Parameters
    ----------
    req : dict
        A representation of an HTTP request. Expected to contain:
            - 'headers': dict, may include 'X-CSRF-Token'
            - 'body': str (JSON) or dict with a 'user_id' key

    Returns
    -------
    bool
        True if the account was removed successfully, otherwise False.
    """
    # Validate CSRF token
    headers = req.get("headers", {})
    csrf_token = headers.get("X-CSRF-Token")
    if csrf_token != EXPECTED_CSRF_TOKEN:
        return False

    # Extract user ID from body
    body = req.get("body")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return False

    user_id = body.get("user_id") if isinstance(body, dict) else None
    if not isinstance(user_id, int):
        return False

    # Attempt to delete the user
    if user_id in database:
        del database[user_id]
        return True

    # User ID not found
    return False